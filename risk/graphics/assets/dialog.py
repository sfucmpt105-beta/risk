import time
import pygame

import risk
import risk.graphics.assets

from risk.graphics.assets.base import BROWN
from risk.graphics.assets.base import PicassoAsset
from risk.graphics.assets.text import TextAsset

class DialogAsset(PicassoAsset):
    def __init__(self, x, y, msg, width=400, height=200, colour=BROWN):
        self.text_asset = TextAsset(0, 0, msg)
        self.colour = colour
        self.background = pygame.Surface((width, height))
        PicassoAsset.__init__(self, None, x, y)

    def draw(self):
        self.background.fill(self.colour)
        self.background.blit(self.text_asset.draw(), (10, 10))
        return self.background

    def set_text(self, msg):
        self.text_asset.render_text(msg)

    def finished(self):
        return True

class BlockingNumericDialogAsset(DialogAsset):
    MAX_LENGTH = 3

    def __init__(self, x, y, msg):
        self.user_input_asset = TextAsset(0, 0, '')
        self.reset()
        DialogAsset.__init__(self, x, y, msg)

    def draw(self):
        background = DialogAsset.draw(self)
        background.blit(self.user_input_asset.draw(), (150, 150))
        return background

    # TODO argh, clean this up!
    def get_user_key_input(self, poll_sleep, default=0):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key = str(event.unicode)
                    if self.is_numeric(key) and len(self.user_input) < \
                            BlockingNumericDialogAsset.MAX_LENGTH:
                        self.user_input += key
                        self.user_input_asset.render_text(self.user_input)
                    elif event.key == pygame.K_BACKSPACE and \
                            len(self.user_input) > 0:
                        self.user_input = self.user_input[:-1]
                        self.user_input_asset.render_text(self.user_input)
                    elif event.key == pygame.K_RETURN:
                        done = True
            time.sleep(poll_sleep)
        if len(self.user_input) > 0:
            return int(self.user_input)
        else:
            return 0

    def reset(self):
        self.user_input = '' 
        self.user_input_asset.render_text(self.user_input)
        
    def is_numeric(self, char):
        return '0' <= char <= '9'
