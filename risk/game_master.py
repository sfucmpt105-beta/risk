import risk.logger
import risk.commands
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

    
    ###########################################################################
    ## Setup actions
    #
    def choose_territories(self):
        pass

    def add_end_turn_callback(self, callback):
        self.end_turn_callbacks.append(callback)

    def generate_human_players(self, number_of_players):
        for i in xrange(number_of_players):
            self.players.append(HumonRiskPlayer("Human %s" % i))
    
    ###########################################################################
    ## Run time events/hooks
    #
    def call_end_turn_callbacks(self):
        risk.logger.debug('Calling end of turn callbacks')
        if not self.ended:
            for callback in self.end_turn_callbacks:
                callback(self)
    
    ###########################################################################
    ## Game state queries
    #
    def number_of_players(self):
        return len(self.players)

    def end_game(self):
        risk.logger.debug('Ending game!')
        self.ended = True

    ###########################################################################
    ## Player actions
    #
    def player_take_turn(self, player_index):
        try:
            self.players[player_index].take_turn(self)
        except IndexError:
            raise NoSuchPlayerError(player_index, self.number_of_players)

    def player_territories(self, player):
        # TODO implement
        return []

    def player_attack(self, player, territory):
        # TODO implement
        return 0, 0

    def player_add_infantry(self, player, territory):
        # TODO implement
        return 0, 0

    def player_add_cavalry(self, player, territory):
        # TODO implement
        return 0, 0

    def player_add_artilery(self, player, territory):
        # TODO implement
        return 0, 0
