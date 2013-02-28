import time
import threading

from datetime import timedelta
from datetime import datetime

import pygame
from pygame.locals import *

import risk
import risk.logger

picasso_instance = None

def get_picasso(*args, **kwargs):
    if not hasattr(get_picasso, 'picasso_instance'):
        setattr(get_picasso, 'picasso_instance', Picasso(*args, **kwargs))
    return getattr(get_picasso, 'picasso_instance')
  

class Picasso(threading.Thread):
    def __init__(self, background='', width=1920, 
                height=1080, fps=30, caption='RiskPy'):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
            
        # convert background for faster draw
        self.background = pygame.image.load(background).convert()
        self.background = \
            pygame.transform.scale(self.background, (width, height))

        self.fps = fps
        self.canvas = []
        self.ended = False

        threading.Thread.__init__(self)

    def run(self):
        _sleep_time = 1.0 / self.fps
        _sleep_delta = timedelta(0, _sleep_time)
        # keep running until interrupted
        try:
            while not self.ended:
                next_frame = datetime.now() + _sleep_delta
                self.draw_canvas()
                time.sleep((next_frame - datetime.now()).total_seconds())
        except Exception as e:
            risk.logger.critical(
                "shit happened in the picasso subsystem! %s" % e)

    def draw_canvas(self):
        self.window.blit(self.background, (0, 0))
        for level in self.canvas:
            for asset in level:
                asset.draw
        pygame.display.flip()

    def end(self):
        risk.logger.debug("received request to terminate graphics subsystem!")
        self.ended = True
