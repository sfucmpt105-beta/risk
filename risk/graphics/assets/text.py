import pygame
from pygame.font import Font

import risk
import risk.logger
from risk.graphics import assets
from risk.graphics.assets.base import PicassoAsset

class TextAsset(PicassoAsset):
    def __init__(self, msg, x, y, colour=assets.base.BLACK, size=32):
        font = Font(None, size)
        surface = font.render(msg, False, colour)
        PicassoAsset.__init__(self, surface, x, y)
