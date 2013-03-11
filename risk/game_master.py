from sets import Set

import risk
import risk.logger
import risk.commands
import risk.battle
import risk.errors
import risk.board

from risk.ai import BasicRiskBot
from risk.errors.game_master import *
from risk.errors.battle import *
from risk.player import HumonRiskPlayer

class GameMaster(object):
    _RISK_RULE_STARTING_RESERVES = 40
    _DEPLOYS_PER_TURN = 5

    def __init__(self, board, settings, num_players=5):
        MIN_PLAYERS = 2
        MAX_PLAYERS = 6
        if not MIN_PLAYERS <= num_players <= MAX_PLAYERS:
            raise risk.errors.RiskGameError('Invalid number of players: %s' %
                num_players)
 
        self.board = board
        # need to setup with settings later
        self.ended = False
        self.end_turn_callbacks = []
        self.end_game_callbacks = []
        self.players = []
        self._current_player = 0
        self._num_players = num_players
        self.callbacks = {
            'start_game': [],
            'start_action': [],
            'start_turn': [],
            'end_action': [],
            'end_turn': [],
            'end_game': [],
        }
        self.add_end_action_callback(GameMaster.check_player_elimination)

    
    ###########################################################################
    ## Internal actions
    #
    def _select_next_player(self):
        self._current_player += 1
        self._current_player %= len(self.players)

    ###########################################################################
    ## Setup actions
    #
    def choose_territories(self):
        risk.logger.debug('Starting territory pick phase...')
        availables = self.board.territories()
        old_current = self._current_player
        self._current_player = 0
        while len(availables) > 0:
            try:
                player = self.current_player()
                choice = player.choose_territory(availables)
                availables[choice].owner = player
                availables[choice].armies = 1
                del(availables[choice])
                self._select_next_player()
            except KeyError:
                if len(choice) > 0:
                    risk.logger.warn("%s is not a valid choice" % choice)
        self._current_player = old_current
        risk.logger.debug('Territory pick complete!')
        self._assign_player_reserves()

    def deploy_troops(self):
        risk.logger.debug('Starting troop deploy phase...')
        for _ in xrange(starting_reserves / self._DEPLOYS_PER_TURN):
            for player in self.players:
                if player.reserves > 0:
                    player.deploy_reserve(self, self._DEPLOYS_PER_TURN)
        risk.logger.debug('Troop deplyoment phase complete!')

    def add_end_turn_callback(self, callback):
        self.callbacks['end_turn'].append(callback)

    def add_end_game_callback(self, callback):
        self.callbacks['end_game'].append(callback)

    def add_start_turn_callback(self, callback):
        self.callbacks['start_turn'].append(callback)

    def add_end_action_callback(self, callback):
        self.callbacks['end_action'].append(callback)

    def generate_players(self, number_of_human_players, gui=False):
        risk.logger.debug("Generating %s human players" % \
            number_of_human_players)

        for i in xrange(number_of_human_players):
            if gui:
                from risk.graphics import player
                self.players.append(
                    risk.graphics.player.HumonGuiRiskPlayer("GHuman %s" % i))
            else:
                self.players.append(HumonRiskPlayer("Human %s" % i))

        risk.logger.debug("Generating %s bots" % \
            (self._num_players - number_of_human_players))

        for i in xrange(self._num_players - number_of_human_players):
            self.players.append(BasicRiskBot(str(i)))

    def _print_available_territories(self):
        territories = self.board.territories()
        while len(territories) > 0:
            choice = self.current_player().pick_territory(territories)

    def _assign_player_reserves(self):
        risk.logger.debug('Giving each player reserves...')
        scaling = (len(self.players) - 2) * 5
        starting_reserves = self._RISK_RULE_STARTING_RESERVES - scaling
        for player in self.players:
            player.reserves = \
                starting_reserves - len(self.player_territories(player))
            risk.logger.debug(
                'Gave [%s] %s reserves' % (player.name, player.reserves))

    
    ###########################################################################
    ## Run time events/hooks
    #
    def call_end_turn_callbacks(self):
        risk.logger.debug('Calling end of turn callbacks')
        if not self.ended:
            for callback in self.callbacks['end_turn']:
                callback(self)

    def call_start_turn_callbacks(self):
        risk.logger.debug('Calling start of turn callback')
        if not self.ended:
            for callback in self.callbacks['start_turn']:
                callback(self)

    def end_turn(self):
        self.call_end_turn_callbacks()
        self._select_next_player()

    def event_action(function):
        risk.logger.debug('Calling end action %s callback' % function)
        def function_with_callback(self, *args):
            result = function(self, *args)
            for callback in self.callbacks['end_action']:
                callback(self, function.func_name, result, args)
            return result
        return function_with_callback

    def check_player_elimination(self, function, result, args):
        if function == 'player_attack':
            if result == True:
                for player in self.players:
                    if len(self.player_territories(player)) == 0:
                        self.eliminate_player(player)

    # TODO fix select next player bug
    def eliminate_player(self, player):
        self.players.remove(player)
        for _ in xrange(10):
            print "%s eliminated!" % player.name

        if len(self.players) <= 1:
            for _ in xrange(100):
                print "%s WINS!!!!" % self.current_player().name
            self.end_game()

    ###########################################################################
    ## Game state queries
    #
    def number_of_players(self):
        return len(self.players)

    def end_game(self):
        risk.logger.debug('Ending game!')
        self.ended = True
        for callback in self.callbacks['end_game']:
            callback(self)

    def current_player(self):
        return self._get_player_with_index(self._current_player)

    def _get_player_with_index(self, index):
        try:
            return self.players[index]
        except IndexError:
            raise NoSuchPlayerError(index, self.number_of_players)


    ###########################################################################
    ## Player actions
    #
    @event_action
    def player_take_turn(self):
        self.call_start_turn_callbacks()
        player = self._get_player_with_index(self._current_player)
        player.reserves += len(self.player_territories(player))
        player.take_turn(self)
    
    @event_action
    def player_territories(self, player):
        # O(n) lookup
        player_territories = {}
        for name, territory in self.board.territories().iteritems():
            if territory.owner == player:
                player_territories[name] = territory
        return player_territories

    @event_action
    def player_attack(self, player, origin_name, target_name):
        origin = self.player_territories(player)[origin_name]
        target = self.board.territories()[target_name]
        success = risk.battle.attack(origin, target)
        return success

    @event_action
    def player_add_army(self, player, territory_name, number_of_armies=1):
        number_of_armies = number_of_armies
        territory = self.board[territory_name]
        if territory.owner != player:
            raise TerritoryNotOwnedByPlayer(territory, player)
        elif player.reserves < number_of_armies:
            raise NotEnoughReserves(player)
        elif number_of_armies < 1:
            raise DeployRangeError(number_of_armies)
        if False:
            pass
        else:
            player.reserves -= number_of_armies
            territory.armies += number_of_armies
            return territory.armies, player.reserves

    @event_action
    def player_move_armies(self, player, origin_territory_name, destination_territory_name, number_of_armies):
        origin_territory = self.board[origin_territory_name]
        destination_territory = self.board[destination_territory_name]
        if origin_territory.owner != player:
            raise TerritoryNotOwnedByPlayer(origin_territory, player)
        elif destination_territory.owner != player:
            raise TerritoryNotOwnedByPlayer(destination_territory, player)
        elif number_of_armies >= origin_territory or number_of_armies < 1:
            raise MoveRangeError(number_of_armies)
        elif not origin_territory.is_connected(destination_territory):
            raise NotConnected(origin_territory, destination_territory)
        else:
            origin_territory.armies -= number_of_armies
            destination_territory.armies += number_of_armies
            return origin_territory.armies, destination_territory.armies
