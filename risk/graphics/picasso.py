import time
import threading
import sets
import sys

from datetime import timedelta
from datetime import datetime

import pygame
from pygame.locals import *

import risk
import risk.logger

from risk.graphics.event import pump
from risk.graphics.assets.base import PicassoAsset
from risk.graphics.assets.text import TextAsset

def get_picasso(*args, **kwargs):
    if not hasattr(get_picasso, 'picasso_instance'):
        get_picasso.picasso_instance = Picasso(*args, **kwargs)
        get_picasso.picasso_instance.daemon = True
    return get_picasso.picasso_instance
  

class Picasso(threading.Thread):
    def __init__(self, background='', width=1920, 
                height=1080, fps=100, caption='RiskPy'):
        pygame.init()
        flags = 0x0
        flags |= pygame.RESIZABLE
        self.window = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(caption)
            
        # convert background for faster draw
        self.background = pygame.image.load(background).convert()
        self.background = \
            pygame.transform.scale(self.background, (width, height))

        self.fps = fps
        self.canvas = {}
        self.ended = False
        self.game_master = None
        
        self.clock = pygame.time.Clock()

        threading.Thread.__init__(self)

    def run(self):
        try:
            while not self.ended:
                self.draw_canvas()
                self.clock.tick(self.fps)
        except Exception as e:
            risk.logger.critical(
                "shit happened in the picasso subsystem! %s" % e)
        pygame.quit()

    def draw_canvas(self):
        pump()
        self.window.blit(self.background, (0, 0))
        # make a deep copy of layers first to avoid race condition where dict
        # size can change during iteration. try to do it lockless, if we're
        # still having issues, fix with mutex
        try:
            for _, level in sorted(self.canvas.iteritems()):
                for asset in level:
                    if isinstance(asset, PicassoAsset):
                        self.window.blit(asset.draw(), asset.get_coordinate())
                    else:
                        risk.logger.warn("None asset detected in canvas, ",
                            "skipping...[%s]" % asset)
        except RuntimeError:
            risk.logger.error("ignoring dictionary size change...")
        fps_asset = self.get_fps_asset()
        self.window.blit(fps_asset.draw(), fps_asset.get_coordinate())
        pygame.display.flip()

    def add_asset(self, layer, asset):
        try:
            self.canvas[layer].add(asset)
        except KeyError:
            self.canvas[layer] = sets.Set()
        finally:
            self.canvas[layer].add(asset)

    def remove_asset(self, layer, asset):
        try:
            self.canvas[layer].remove(asset)
        except KeyError:
            pass


    def end(self):
        risk.logger.debug("received request to terminate graphics subsystem!")
        self.ended = True

    def get_fps_asset(self):
        asset = TextAsset(1050, 16, "%s FPS" % int(self.clock.get_fps()), 
                (255, 255, 0), 32)
        return asset
