import pygame

import risk
import risk.logger
import risk.graphics.assets

from risk.graphics.assets import base
from risk.graphics.assets.base import PicassoAsset
from risk.graphics.assets.clickable import ClickableAsset

TERRITORY_ART_ASSET_PATH = './assets/art/territories/'
NO_PLAYER_COLOUR = base.BLACK

def build_territory_asset(continent, territory, x, y):
    full_path = "%s/%s/%s.png" % \
            (TERRITORY_ART_ASSET_PATH, continent, territory.name)
    return TerritoryAsset(continent, territory, full_path, x, y)

def build_player_colour_mapping(players):
    overflow_colour = base.BLACK
    colours = [
        base.RED,
        base.GREEN,
        base.BLUE,
        base.YELLOW,
        base.PURPLE,
        base.ORANGE,
    ]
    risk.logger.debug("assigning player colours...")
    TerritoryAsset.mapping = {}
    for player in players:
        try:
            colour = colours.pop()
            risk.logger.debug("assigning %s with %s" % (player.name, colour))
            TerritoryAsset.mapping[player] = colour
        except IndexError:
            risk.logger.error("no more colours left, assigning %s with %s!" \
                    % (player.name, overflow_colour))
            TerritoryAsset.mapping[player] = overflow_colour

class TerritoryAsset(ClickableAsset):
    def __init__(self, continent, territory, image_path, x, y):
        self.territory = territory
        surface = pygame.image.load(image_path)
        PicassoAsset.__init__(self, surface, x, y)
     
    def mouse_hovering(self):
        mouse_position = pygame.mouse.get_pos()
        adjusted_position = (mouse_position[0] - self.x,
                mouse_position[1] - self.y)
        return ClickableAsset.mouse_hovering(self) and \
                self.surface.get_at(adjusted_position)[3]

    def _normal_surface(self):
        owner = self.territory.owner
        colour = NO_PLAYER_COLOUR
        try:
            colour = TerritoryAsset.mapping[owner]
        except KeyError:
            risk.logger.error("no colours assigned to %s" % owner.name)

        barray = pygame.surfarray.pixels3d(self.surface)
        barray[:,:,0] = colour[0]
        barray[:,:,1] = colour[1]
        barray[:,:,2] = colour[2]
        return self.surface
        
    def _highlighted_surface(self):
        highlight_factor = 120
        barray = pygame.surfarray.pixels3d(self._normal_surface())
        if 255 - barray[:,:,0][0][0] >= highlight_factor:
            barray[:,:,0] += highlight_factor
        if 255 - barray[:,:,1][0][0] >= highlight_factor:
            barray[:,:,1] += highlight_factor
        if 255 - barray[:,:,2][0][0] >= highlight_factor:
            barray[:,:,2] += highlight_factor
        return self.surface

TerritoryAsset.mapping = {}
