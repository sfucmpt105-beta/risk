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

        threading.Thread.__init__(self)

    def run(self):
        _sleep_time = 1.0 / self.fps
        _sleep_delta = timedelta(0, _sleep_time)
        # keep running until interrupted
        try:
            while not self.ended:
                next_frame = datetime.now() + _sleep_delta
                self.draw_canvas()
                time_until_next_frame = \
                    (next_frame - datetime.now()).total_seconds()
                if time_until_next_frame > 0:
                    time.sleep(time_until_next_frame)
        except Exception as e:
            risk.logger.critical(
                "shit happened in the picasso subsystem! %s" % e)

    def draw_canvas(self):
        pygame.event.pump()
        self.window.blit(self.background, (0, 0))
        for level in sorted(self.canvas.keys()):
            for asset in self.canvas[level]:
                if isinstance(asset, PicassoAsset):
                    self.window.blit(asset.draw(), asset.get_coordinate())
                else:
                    risk.logger.warn("None asset detected in canvas, ",
                        "skipping...[%s]" % asset)
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
        if not hasattr(Picasso, '_fps_start_time'):
            Picasso._fps_start_time = datetime.now()
        if not hasattr(Picasso, '_fps_frames'):
            Picasso._fps_frames = 0

        Picasso._fps_frames += 1
        total_elapsed = (datetime.now() - \
            Picasso._fps_start_time).total_seconds()
        if total_elapsed < 1:
            total_elapsed = 1
        average_fps = float(Picasso._fps_frames) / total_elapsed
        asset = TextAsset(1050, 16, "%s FPS" % int(average_fps), 
                (255, 255, 0), 32)
        return asset
