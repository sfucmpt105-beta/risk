import pygame
from pygame.font import Font

import risk
import risk.logger
import risk.graphics.assets

from risk.graphics.assets import base
from risk.graphics.assets.base import PicassoAsset
from risk.graphics.assets.clickable import ClickableAsset
from risk.graphics.assets.text import TextAsset

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
        self.last_known_owner = None
        self.highlighted = False
        surface = pygame.image.load(image_path).convert_alpha()
        PicassoAsset.__init__(self, surface, x, y)
     
    def mouse_hovering(self, mouse_pos=None):
        if not mouse_pos:
            mouse_pos = pygame.mouse.get_pos()
        adjusted_position = (mouse_pos[0] - self.x,
                mouse_pos[1] - self.y)
        # needs and true otherwise python returns an int value, ugh!
        try:
            return ClickableAsset.mouse_hovering(self) and \
                    self.surface.get_at(adjusted_position)[3] and True
        except IndexError:
            return False

    def _normal_surface(self):
        owner = self.territory.owner
        colour = NO_PLAYER_COLOUR
        try:
            colour = TerritoryAsset.mapping[owner]
        except KeyError:
            risk.logger.error("no colours assigned to %s" % owner.name)
        if self.dirty():
            barray = pygame.surfarray.pixels3d(self.surface)
            barray[:,:,0] = colour[0]
            barray[:,:,1] = colour[1]
            barray[:,:,2] = colour[2]
            self.highlighted = False
        return self.surface
        
    def _highlighted_surface(self):
        highlight_factor = 120
        if self.dirty():
            barray = pygame.surfarray.pixels3d(self._normal_surface())
            if 255 - barray[:,:,0][0][0] >= highlight_factor:
                barray[:,:,0] += highlight_factor
            if 255 - barray[:,:,1][0][0] >= highlight_factor:
                barray[:,:,1] += highlight_factor
            if 255 - barray[:,:,2][0][0] >= highlight_factor:
                barray[:,:,2] += highlight_factor
            self.highlighted = True
        return self.surface

    def dirty(self):
        return self.last_known_owner != self.territory.owner or \
                self.highlighted != self.mouse_hovering()

TerritoryAsset.mapping = {}


class ArmyCountAsset(PicassoAsset):
    def __init__(self, territory_asset, size=32):
        self.territory_asset = territory_asset
        self.count = None
        self.size = size
        self.colour = base.BLACK
        x = territory_asset.x + territory_asset.surface.get_width() / 2
        y = territory_asset.y + territory_asset.surface.get_height() / 3
        PicassoAsset.__init__(self, None, x, y)
        # kinda hacky, we have to rebuild the surface to centre the counter

    def draw(self):
        if self.dirty():
            self.count = self.territory_asset.territory.armies
            font = Font(None, self.size)
            self.surface = font.render(str(self.count), False, 
                    self.colour).convert()
        return self.surface

    def dirty(self):
        return self.count != self.territory_asset.territory.armies

