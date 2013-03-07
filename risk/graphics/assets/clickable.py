import pygame
from pygame import Rect
from pygame import mouse
from pygame.font import Font

import risk.graphics.assets
from risk.graphics.assets import base
from risk.graphics.assets.base import PicassoAsset

class ClickableAsset(PicassoAsset):
    def __init__(self, x, y, width, height, msg, size=32, 
            text_colour=base.BLACK, bg_colour=base.WHITE, 
            highlight_text=base.WHITE, highlight_bg=base.BLACK):

        font = Font(None, size)
        self.normal = pygame.Surface((width, height))
        self.normal.fill(bg_colour)
        self.normal.blit(font.render(msg, False, text_colour), (0, 0))
    
        self.highlighted = pygame.Surface((width, height))
        self.highlighted.fill(highlight_bg)
        self.highlighted.blit(font.render(msg, False, highlight_text), (0, 0))
        PicassoAsset.__init__(self, self.normal, x, y)

    def draw(self):
        if self.mouse_hovering():
            return self._highlighted_surface()
        else:
            return self._normal_surface()

    def mouse_hovering(self, mouse_pos=None):
        # pygame gets pissy if it's not initialized so we can't have x and
        # y in the initializer
        if not mouse_pos:
            mouse_pos = mouse.get_pos()
        # srsly???
        return self.surface.get_rect().move(self.x, self.y).collidepoint(
        mouse_pos)

    def _normal_surface(self):
        return self.normal

    def _highlighted_surface(self):
        return self.highlighted
