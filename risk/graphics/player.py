import pygame

import risk
import risk.graphics
import risk.graphics.input
import risk.graphics.assets.text
import risk.graphics.picasso
import risk.player

from risk.player import HumonRiskPlayer
from risk.graphics.input import reinforce_phase
from risk.graphics.input import attack_phase
from risk.graphics.input import fortify_phase
from risk.graphics.assets.text import TextAsset
from risk.graphics.picasso import get_picasso

LAYER = '5_player_feedback'

class HumonGuiRiskPlayer(HumonRiskPlayer):
    def __init__(self, name):
        HumonRiskPlayer.__init__(self, name)

    def reinforce(self, game_master):
        #self.reserves = 0
        #for territory in game_master.player_territories(self).values():
        #    territory.armies = 100
        #picasso = get_picasso()
        #phase_asset = TextAsset(400, 600, 'reinforcing...')
        #picasso.add_asset(LAYER, phase_asset)
        risk.logger.debug("starting reinforcement phase")
        risk.graphics.input.handle_user_mouse_input(game_master, 
                reinforce_phase)

    def attack(self, game_master):
        risk.logger.debug("starting attack phase")
        #phase_asset.render_text('attacking...')
        risk.graphics.input.handle_user_mouse_input(game_master, attack_phase)

    def fortify(self, game_master):
        risk.logger.debug("starting fortify phase")
        #phase_asset.render_text('fortifying...')
        risk.graphics.input.handle_user_mouse_input(game_master, fortify_phase)
        risk.logger.debug("GUI player finished turn!")
        #picasso.remove_asset(LAYER, phase_asset)
