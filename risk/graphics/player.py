import pygame

import risk
import risk.graphics
import risk.graphics.input
import risk.player
from risk.player import HumonRiskPlayer

class HumonGuiRiskPlayer(HumonRiskPlayer):
    def __init__(self, name):
        HumonRiskPlayer.__init__(self, name)

    def take_turn(self, game_master):
        risk.graphics.input.handle_user_input(game_master)
