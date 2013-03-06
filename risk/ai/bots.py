import random

import risk.logger
from risk.player import AbstractRiskPlayer

class BasicRiskBot(AbstractRiskPlayer):
    def __init__(self, title):
        AbstractRiskPlayer.__init__(self, "bot[%s]" % title)

    def choose_territories(self, board):
        raise NotImplementedError

    def take_turn(self, game_master):
        self._deploy_reserves(game_master)
        self._attack_all_possible_targets(game_master)

    def deploy_reserves(self, game_master):
        # evenly distributes
        territories = game_master.player_territories(self)
        idx = 0
        while self.reserves > 0:
            game_master.player_add_army(self, territories[idx], 1)
            idx = (idx + 1) % len(territories)

    def _deploy_reserves(self, game_master):
        # simple uniform distribution of armies
        territories = game_master.player_territories(self).values()
        while self.reserves > 0:
            for territory in territories:
                if self.reserves > 0:
                    game_master.player_add_army(self, territory.name)
                

    def _attack_all_possible_targets(self, game_master):
        territories = game_master.player_territories(self)
        for name, territory in territories.iteritems():
            if territory.armies > 2:
                risk.logger.debug("%s going to attack from %s" % 
                    (self.name, name))
                targets = territory.neighbours.values()
                targets = filter(lambda x: x.owner != self, targets)
                targets = [t.name for t in targets]
                if len(targets) > 0:
                    choice = random.randint(0, len(targets) - 1)
                    game_master.player_attack(self, name, targets[choice])
                else:
                    risk.logger.debug("nowhere to attack!")
            else:
                risk.logger.debug("not enough armies in %s" % name)
