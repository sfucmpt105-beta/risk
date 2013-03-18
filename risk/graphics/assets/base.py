import pygame
from pygame import Surface

BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

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
