import pygame

import risk
from risk.graphics.assets.base import PicassoAsset

ON=True
OFF=False

class ImageAsset(PicassoAsset):
    def __init__(self, x, y, path, scale_x=1.0, scale_y=1.0):
        self.path = path
        self.surface = pygame.image.load(path).convert_alpha()
        if scale_x != 1 or scale_y != 1:
            self.surface = pygame.transform.scale(self.surface, 
                (int(self.surface.get_width() * scale_x),
                int(self.surface.get_height() * scale_y)))
        PicassoAsset.__init__(self, self.surface, x, y)

class ScaledImageAsset(ImageAsset):
    def __init__(self, x, y, width, height, path):
        ImageAsset.__init__(self, x, y, path)
        self.surface = pygame.transform.scale(self.surface, (width, height))

class ToggleImageAsset(ImageAsset):
    def __init__(self, x, y, path, start_state=ON):
        ImageAsset.__init__(self, x, y, path)
        self.state = start_state
        self.blank = pygame.Surface((0, 0), pygame.SRCALPHA, 32)
    
    def draw(self):
        if self.state == ON:
            return self.surface
        else:
            return self.blank

    def toggle(self):
        self.state = not self.state

    def set_state(self, state):
        self.state = state
