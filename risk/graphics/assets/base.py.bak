import pygame
from pygame import Surface

GREY = (190, 190, 190)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
RED = (178, 34, 34)
GREEN = (0, 51, 25)
BLUE = (0, 51, 102)
YELLOW = (204, 204, 0)
PURPLE = (102, 0, 102)
ORANGE = (204, 102, 0)
LIGHT_BROWN = (238, 223, 204)

class PicassoAsset(Surface):
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.surface = surface

    def get_coordinate(self):
        return (self.x, self.y)

    def draw(self):
        return self.surface

    def _update(self):
        pass

    def get_width(self):
        return self.surface.get_width()

    def get_height(self):
        return self.surface.get_height()

class ColourBlockAsset(PicassoAsset):
    def __init__(self, x, y, width, height, colour):
        surface = pygame.Surface((width, height))
        surface.fill(colour)
        PicassoAsset.__init__(self, surface, x, y)

    def set_colour(self, colour):
        self.surface.fill(colour)
