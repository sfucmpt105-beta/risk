import risk.logger
import risk.commands
from risk.ai import RiskBot

class GameMaster(object):
    def __init__(self, board, settings, num_ai=7):
        self.board = board
        # need to setup with settings later
        self.bots = [RiskBot() for i in xrange(num_ai)]
        risk.logger.debug(
            'Game master instance created with %s bots!' % num_ai)
        self.ended = False
    
    def choose_territories(self):
        pass

    def handle_user(self):
        risk.commands.prompt_user(self)       

    def end_game(self):
        risk.logger.debug('Ending game!')
        self.ended = True

    def end_turn(self):
        if not self.ended:
            risk.logger.debug('Ending turn...')
            results = [bot.take_turn(self.board) for bot in self.bots]
            return results

    
