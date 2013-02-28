import pygame
from pygame import Surface

class PicassoAsset(Surface):
    def __init__(self, dimension, coordinate):
        self.x = coordinate[0]
        self.y = coordinate[1]
        self.width = dimension[0]
        self.heigh = dimension[1]

        Surface.__init__(self, dimension)

    def get_coordinate(self):
        return (self.x, self.y)
