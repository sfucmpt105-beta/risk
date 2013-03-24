import pygame
from pygame import Surface

BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
RED = (178, 34, 34)
GREEN = (0, 51, 25)
BLUE = (0, 51, 102)
YELLOW = (204, 204, 0)
PURPLE = (102, 0, 102)
ORANGE = (204, 102, 0)

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
