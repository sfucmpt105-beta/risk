import time

import pygame

import risk
import risk.graphics.event
import risk.graphics.assets

from risk.graphics.event import pump, wait_for_event
from risk.graphics.assets.base import BROWN
from risk.graphics.assets.dialog import DialogAsset
from risk.graphics.assets.text import TextAsset

class PopupDialogAsset(DialogAsset):
    HINT_OFFSET_Y = 30
    def __init__(self, x, y, title, msg, width=400, height=200, colour=BROWN):
        DialogAsset.__init__(self, x, y, title, width, height, colour)
        self.add_text(None, None, msg)
        self.add_text(None, self.dialog_height() - self.HINT_OFFSET_Y, 
                "Click anywhere to continue...")

    def get_confirmation(self):
        confirmed = False
        while not confirmed:
            event = wait_for_event()
            if event.type == pygame.MOUSEBUTTONDOWN and \
                    self.being_dragged(event.pos):
                self.drag_dialog()
            elif event.type == pygame.MOUSEBUTTONUP and not \
                    self.being_dragged(event.pos):
                confirmed = True

