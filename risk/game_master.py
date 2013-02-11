from sets import Set

import risk.logger
import risk.commands
import risk.battle
import risk.errors
import risk.board

from risk.ai import RiskBot
from risk.errors.game_master import *
from risk.player import HumonRiskPlayer

class GameMaster(object):
    def __init__(self, board, settings, num_ai=7):
        self.board = board
        # need to setup with settings later
        self.bots = [RiskBot() for i in xrange(num_ai)]
        risk.logger.debug(
            'Game master instance created with %s bots!' % num_ai)
        self.ended = False
        self.end_turn_callbacks = []
        self.players = []
        self._current_player = 0

    
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
        current = 0
        while len(availables) > 0:
            try:
                player = self.players[current]
                choice = player.choose_territory(availables)
                availables[choice].owner = player
                availables[choice].armies = 1
                del(availables[choice])
                current = (current + 1) % len(self.players)
            except KeyError:
                if len(choice) > 0:
                    risk.logger.warn("%s is not a valid choice" % choice)
        risk.logger.debug('Territory pick complete!')

    def deploy_troops(self):
        _RISK_RULE_STARTING_RESERVES = 40
        _DEPLOYS_PER_TURN = 5
        risk.logger.debug('Starting troop deploy phase...')
        scaling = (len(self.players) - 2) * 5
        starting_reserves = _RISK_RULE_STARTING_RESERVES - scaling
        for player in self.players:
            player.reserves = starting_reserves
        for _ in xrange(starting_reserves / _DEPLOYS_PER_TURN):
            for player in self.players:
                for _ in xrange(_DEPLOYS_PER_TURN):
                    if player.reserves > 0:
                        player.deploy_reserve(self)
        risk.logger.debug('Troop deplyoment phase complete!')

    def add_end_turn_callback(self, callback):
        self.end_turn_callbacks.append(callback)

    def generate_human_players(self, number_of_players):
        MIN_PLAYERS = 2
        MAX_PLAYERS = 6
        if not MIN_PLAYERS <= number_of_players <= MAX_PLAYERS:
            raise risk.errors.RiskGameError('Invalid number of players: %s' %
                                            number_of_players)
        for i in xrange(number_of_players):
            self.players.append(HumonRiskPlayer("Human %s" % i))

    def _print_available_territories(self):
        territories = self.board.territories()
        while len(territories) > 0:
            choice = self.current_player().pick_territory(territories)
    
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
        self._get_player_with_index(self._current_player).take_turn(self)
    
    def player_territories(self, player):
        # O(n) lookup
        player_territories = {}
        for name, territory in self.board.territories().iteritems():
            if territory.owner == player:
                player_territories[name] = territory
        return player_territories

    def player_attack(self, player, origin, target):
        battle= risk.battle.Battle(origin,target)
        risk.battle.Battle.attack(battle)

        return 0, 0

    def player_add_army(self, player, territory_name):
        territory = self.board[territory_name]
        if territory.owner != player:
            raise TerritoryNotOwnedByPlayer(territory, player)
        elif player.reserves < 1:
            raise NotEnoughReserves(player)
        else:
            player.reserves -= 1
            territory.armies += 1
            return territory.armies, player.reserves
