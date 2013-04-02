import pygame
from pygame.font import Font

import risk
import risk.logger
from risk.graphics import assets
from risk.graphics.assets.base import PicassoAsset
_FONT = 'resources/Vera.ttf'

class TextAsset(PicassoAsset):

    def __init__(self, x, y, msg, colour=assets.base.BLACK, size=32, 
            bold=False):
        self.colour = colour
        self.size = size
        self.bold = bold
        PicassoAsset.__init__(self, None, x, y)
        self.render_text(msg)

    def render_text(self, msg):
        font = Font(_FONT, self.size)
        font.set_bold(self.bold)
        self.surface = font.render(msg, False, self.colour)

class CurrentPlayerAsset(TextAsset):
    def __init__(self, x, y, game_master):
        self.game_master = game_master
        self.current = None
        TextAsset.__init__(self, x, y, '')
    
    def draw(self):
        if self.dirty():
            self.current = self.game_master.current_player()
            self.render_text("%s is taking turn..." % self.current.name)
        return TextAsset.draw(self)

    def dirty(self):
        return self.current != self.game_master.current_player()
