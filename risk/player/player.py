import risk
import risk.logger

from risk import commands
from risk.printer import risk_input
from risk.errors.board import *
from risk.errors.game_master import *

class AbstractRiskPlayer(object):
    def __init__(self, name):
        self.name = name
        self.is_bot = False
        self.reserves = 0

    def take_turn(self, game_master):
        raise NotImplementedError

    def choose_territory(self, available):
        raise NotImplementedError
    
    def deploy_reserve(self, game_master):
        raise NotImplementedError

# Qwerrrrrrk
class HumonRiskPlayer(AbstractRiskPlayer):
    def __init__(self, name):
        # Python sucks at this, base refers to base class
        AbstractRiskPlayer.__init__(self, name)

    def take_turn(self, game_master):
        commands.prompt_user(self, game_master)

    def choose_territory(self, availables):
        print "%s's turn..." % self.name
        return commands.prompt_choose_territory(availables)

    def deploy_reserve(self, game_master, max_deploys=0):
        player_picked = False
        deploys = self.reserves if self.reserves < max_deploys else max_deploys
        while deploys > 0:
            choice, number_of_deploys = \
                commands.prompt_deploy_reserves(self, game_master, deploys)
            try:
                game_master.player_add_army(self, choice, number_of_deploys)
                deploys -= number_of_deploys
            except (TerritoryNotOwnedByPlayer, NotEnoughReserves, 
                NoSuchTerritory) as e:
                risk.logger.error(str(e))
