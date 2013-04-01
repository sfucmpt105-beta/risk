import pygame
from pygame import Rect
from pygame import mouse
from pygame.font import Font

import risk.graphics.assets
import risk.graphics.event
from risk.graphics.assets import base
from risk.graphics.assets.base import PicassoAsset
from risk.graphics.event import wait_for_mouse_release
_FONT = 'resources/Vera.ttf'

class ClickableAsset(PicassoAsset):
    def __init__(self, x, y, width, height, msg, size=16, 
            text_colour=base.BLACK, bg_colour=base.WHITE, 
            highlight_text=base.WHITE, highlight_bg=base.BLACK,
            offset_x=0, offset_y=0):

        self.normal = pygame.Surface((width, height))
        self.normal.fill(bg_colour)

        font = Font(_FONT, size)
        font_width, font_height = font.size(msg)
        font_x = (width - font_width) / 2
        font_y = (height - font_height) / 2

        self.normal.blit(font.render(msg, False, text_colour), 
                                    (font_x, font_y))

        self.highlighted = pygame.Surface((width, height))
        self.highlighted.fill(highlight_bg)
        self.highlighted.blit(font.render(msg, False, highlight_text), 
                                        (font_x, font_y))

        self.offset_x = offset_x
        self.offset_y = offset_y
        
        self.force_highlight = False
        self.disabled = False
        PicassoAsset.__init__(self, self.normal, x, y)

    def draw(self):
        if self.force_highlight or (self.mouse_hovering() and \
                not self.disabled):
            return self._highlighted_surface()
        else:
            return self._normal_surface()

    def mouse_hovering(self, mouse_pos=None):
        # pygame gets pissy if it's not initialized so we can't have x and
        # y in the initializer
        if not mouse_pos:
            mouse_pos = mouse.get_pos()
        # srsly???
        return self.surface.get_rect().move(
            self.x + self.offset_x, 
            self.y + self.offset_y).collidepoint(
                mouse_pos) and not self.disabled

    # take control of main thread until mouse released
    def confirmed_click(self):
        release = wait_for_mouse_release()
        return self.mouse_hovering(release.pos)

    def _normal_surface(self):
        return self.normal

    def _highlighted_surface(self):
        return self.highlighted
