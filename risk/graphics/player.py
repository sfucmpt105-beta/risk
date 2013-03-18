import pygame

import risk
import risk.graphics
import risk.graphics.input
import risk.player

from risk.player import HumonRiskPlayer
from risk.graphics.input import reinforce_phase
from risk.graphics.input import attack_phase
from risk.graphics.input import fortify_phase

class HumonGuiRiskPlayer(HumonRiskPlayer):
    def __init__(self, name):
        HumonRiskPlayer.__init__(self, name)

    def take_turn(self, game_master):
        #self.reserves = 0
        #for territory in game_master.player_territories(self).values():
        #    territory.armies = 100
        risk.logger.debug("starting reinforcement phase")
        risk.graphics.input.handle_user_mouse_input(game_master, 
                reinforce_phase)
        risk.logger.debug("starting attack phase")
        risk.graphics.input.handle_user_mouse_input(game_master, attack_phase)
        risk.logger.debug("starting fortify phase")
        risk.graphics.input.handle_user_mouse_input(game_master, fortify_phase)
        risk.logger.debug("GUI player finished turn!")
