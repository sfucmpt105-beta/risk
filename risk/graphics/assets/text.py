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

# supports multiline
class CentredTextAsset(TextAsset):
        def __init__(self, x, y, width, height, msg, 
                colour=assets.base.BLACK, size=32, bold=False):
            self.width = width
            self.height = height
            TextAsset.__init__(self, x, y, msg, colour, size, bold)

        def render_text(self, msg):
            font = Font(_FONT, self.size)
            font.set_bold(self.bold)
            new_surface = pygame.Surface((self.width, self.height), 
                            pygame.SRCALPHA, 32)
            msg = msg.strip("\n")
            lines = msg.split("\n")
            longest = max(lines, key=lambda x: len(x))
            
            #new_surface = pygame.Surface((self.width, self.height))
            temp_surface = font.render(longest, False, self.colour)
            msg_width = temp_surface.get_size()[0]
            msg_height = font.get_height() * len(lines)
            msg_x = (new_surface.get_width() - msg_width) / 2
            msg_y = (new_surface.get_height() - msg_height) / 2
            for index, line in enumerate(lines):
                font_surface = font.render(line, False, self.colour)
                new_surface.blit(font_surface, (msg_x, 
                        msg_y + (font.get_height() * index)))
            self.surface = new_surface


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
