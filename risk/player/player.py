import risk
import risk.logger

from risk import commands
from risk.printer import risk_input
from risk.errors.board import *
from risk.errors.game_master import *

from risk.commands import reinforce_commands
from risk.commands import attack_commands

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
        while self.reserves > 0:
            print 'player has armies to deploy'
            print "%s's territories: " % self.name
            print "---------------------------------------------------"
            print game_master.player_territories(self).keys()
            risk.printer.display_user_armies(self, 
                    game_master.player_territories(self))
            commands.prompt_user(self, game_master, 
                    reinforce_commands, HumonRiskPlayer._no_more_reserves)
        commands.prompt_user(self, game_master, attack_commands)

    def choose_territory(self, availables):
        print "%s's turn..." % self.name
        return commands.prompt_choose_territory(availables)

    def deploy_reserve(self, game_master, max_deploys=0):
        player_picked = False
        deploys = self.reserves if self.reserves < max_deploys else max_deploys
        while deploys > 0:
            choice, number_of_deploys = \
                commands.prompt_deploy_reserves(self, game_master, deploys)
            if number_of_deploys > deploys:
                risk.logger.error(
                    "cannot deploy %s armies, %s is the max" % \
                    (number_of_deploys, deploys))
            else:
                deploys -= self._deploy_reserves_helper(
                    game_master, choice, number_of_deploys)

    def _deploy_reserves_helper(self,game_master, choice, number_of_deploys):
        _FAILED = 0
        try:
            game_master.player_add_army(self, choice, number_of_deploys)
            return number_of_deploys
        except (TerritoryNotOwnedByPlayer, NotEnoughReserves, 
            NoSuchTerritory) as e:
            risk.logger.error(str(e))
        return _FAILED
    
    @staticmethod
    def _no_more_reserves(player, game_master):
        return player.reserves <= 0
