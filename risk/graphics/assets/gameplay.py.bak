import pygame

import risk

import risk.graphics.assets

from .base import PicassoAsset
from .base import WHITE, LIGHT_BROWN
from .text import TextAsset
from .territory import TerritoryAsset

DEFAULT_WIDTH = 250
DEFAULT_HEIGHT = 140
DEFAULT_X_OFFSET = 5
COLOUR_BLOCK_WIDTH = 10

class PlayersAsset(PicassoAsset):
    def __init__(self, x, y, game_master):
        PicassoAsset.__init__(self, None, x, y)

        self.game_master = game_master
        self.known_players = self.game_master.players
        self.update()

    def draw(self):
        return self.surface

    # TODO CLEANUP, SRSLY!
    def update(self):
        current_step = 0
        stride = DEFAULT_HEIGHT / len(self.known_players)
        new_view = pygame.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT),
                                    pygame.SRCALPHA, 32)
        for player in self.known_players:
            if player == self.game_master.current_player():
                highlight = pygame.Surface((new_view.get_width(), 
                            stride - 5))
                highlight.fill(LIGHT_BROWN)
                new_view.blit(highlight, (0, current_step))
            # account for player elimination
            if player in self.game_master.players:
                text_asset = TextAsset(0, 0, player.name, size=16, bold=True)
                army_count_asset = TextAsset(0, 0, str(len(self.game_master.player_territories(player))), size=16,
                                    bold=True)
                colour_block = pygame.Surface((COLOUR_BLOCK_WIDTH, stride))
                colour = TerritoryAsset.mapping[player]
                colour_block.fill(colour)
                new_view.blit(text_asset.draw(), (DEFAULT_X_OFFSET + COLOUR_BLOCK_WIDTH, 
                    current_step))
                new_view.blit(army_count_asset.draw(), (new_view.get_width() - army_count_asset.get_width() - 5, current_step))
                new_view.blit(colour_block, (0, current_step - 5))
                current_step += stride

        self.surface = new_view
