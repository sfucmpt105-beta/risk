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

    def move_after_attack(self, game_master, origin_name, target_name):
        origin = game_master.player_territories(self)[origin_name]
        #split armies into 2
        moveable_armies = origin.armies - 1
        armies_to_move = (moveable_armies / 2) +1
        if armies_to_move == 0:
            armies_to_move = 1
        origin_armies, destination_armies = game_master.player_move_armies(self, origin_name, target_name, int(armies_to_move))
        risk.logger.debug("%s now has: %s armies" %(origin_name, origin_armies))
        risk.logger.debug("%s now has: %s armies" %(target_name, destination_armies))

               

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
                    success = game_master.player_attack(self, name, targets[choice])
                    if success:
                        self.move_after_attack(game_master, name, targets[choice])
                else:
                    risk.logger.debug("nowhere to attack!")
            else:
                risk.logger.debug("not enough armies in %s" % name)

class CurtisRiskBot(BasicRiskBot):
    def __init__(self, title):
        BasicRiskBot.__init__(self, "Curtis Bot[$s]" %title)
    
    def number_of_turns(self):
        number_of_turns += 1
        return number_of_turns
        
    def take_turn(self, game_master):
        number_of_turns = self.number_of_turns()
        self.deploy_reserves(game_master, number_of_turns)

    def deploy_reserves(self, game_master, number_of_turns):
        self.deploy_order(game_master, number_of_turns, 'north_america')
        self.deploy_order(game_master, number_of_turns, 'south_america')
        self.deploy_order(game_master, number_of_turns, 'australia')
        self.deploy_order(game_master, number_of_turns, 'africa')
        self.deploy_order(game_master, number_of_turns, 'europe')
        self.deploy_order(game_master, number_of_turns, 'asia')
    
    def number_to_deploy(self, game_master, territory):
        if territory.armies > self.reserves and self.reserves > 0:
            game_master.player_add_army(self, territory.name, self.reserves)
        elif territory.armies <= self.reserves and self.reserves > 0:
            to_add = 0
            
        return number_to_deploy
        
    def deploy_order(self, game_master, number_of_turns, continent):
        continent_owned = 1
        hit_list = []
        for territory in game_master.board.continents[continent].values():
            if self.reserves > 0 and territory.owner != self:
                continent_owned = 0
                return hit_list.append(territory.name)
                    
        while self.reserves > 0 and continent_owned == 1:
            if continent == 'north_america':
                territory = game_master.board.territory['venezuela']
                if territory.owner != self:
                    game_master.player_add_army(self, 'central_america', half_of_reserves)
                territory = game_master.board.territory['iceland']
                if territory.owner != self:
                    to_add = 0
                    
            
        if number_of_turns < 10:
            for territory in game_master.board.continents[continent].values():
                if self.reserves > 0:
                    if territory.owner == self:
                        print self.reserves
                        game_master.player_add_army(self, territory.name, self.reserves)
        if number_of_turns > 10:
            for territory in game_master.board.continents[continent].values():
                if self.reserves > 0:
                    if territory.owner != self:
                        break