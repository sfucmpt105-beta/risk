from sets import Set

import risk.logger
import risk.commands
import risk.battle
import risk.errors
import risk.board

from risk.ai import BasicRiskBot
from risk.errors.game_master import *
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
        self.end_turn_callbacks.append(callback)

    def add_end_game_callback(self, callback):
        self.end_game_callbacks.append(callback)

    def generate_players(self, number_of_human_players):
        risk.logger.debug("Generating %s human players" % \
            number_of_human_players)

        for i in xrange(number_of_human_players):
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
            for callback in self.end_turn_callbacks:
                callback(self)

    def end_turn(self):
        self._select_next_player()

    ###########################################################################
    ## Game state queries
    #
    def number_of_players(self):
        return len(self.players)

    def end_game(self):
        risk.logger.debug('Ending game!')
        self.ended = True
        for callback in self.end_game_callbacks:
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
    def player_take_turn(self):
        player = self._get_player_with_index(self._current_player)
        player.reserves += len(self.player_territories(player))
        player.take_turn(self)
    
    def player_territories(self, player):
        # O(n) lookup
        player_territories = {}
        for name, territory in self.board.territories().iteritems():
            if territory.owner == player:
                player_territories[name] = territory
        return player_territories

    def player_attack(self, player, origin_name, target_name):
        origin = self.player_territories(player)[origin_name]
        target = self.board.territories()[target_name]
        success = risk.battle.attack(origin, target)
        return success

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

    def player_fortify(self, player, origin_name, target_name):
        origin = self.player_territories(player)[origin_name]
        return 0,0  
