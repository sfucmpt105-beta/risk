import pygame

import risk
from risk.graphics.assets.base import PicassoAsset

class ImageAsset(PicassoAsset):
    def __init__(self, x, y, path, scale_x=1.0, scale_y=1.0):
        self.path = path
        self.surface = pygame.image.load(path).convert_alpha()
        if scale_x != 1 or scale_y != 1:
            self.surface = pygame.transform.scale(self.surface, 
                (int(self.surface.get_width() * scale_x),
                int(self.surface.get_height() * scale_y)))
        PicassoAsset.__init__(self, self.surface, x, y)
