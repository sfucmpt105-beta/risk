import time
import pygame

import risk
import risk.graphics.assets

from risk.graphics.picasso import get_picasso
from risk.graphics.event import wait_for_event
from risk.graphics.event import pump
from risk.graphics.assets.base import BLACK, BROWN, WHITE
from risk.graphics.assets.base import PicassoAsset
from risk.graphics.assets.text import TextAsset
from risk.graphics.assets.clickable import ClickableAsset

class DialogAsset(PicassoAsset):
    _BORDER_PIXELS = 5
    _TITLE_HEIGHT_PIXELS = 25

    def __init__(self, x, y, title, width=400, height=200, colour=BROWN):
        self.colour = colour
        self.background = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self.title = ClickableAsset(
            self._BORDER_PIXELS,
            self._BORDER_PIXELS,
            width - 2 * self._BORDER_PIXELS,
            self._TITLE_HEIGHT_PIXELS - self._BORDER_PIXELS,
            " == %s == " % title,
            size=16,
        )
        self.title.offset_x = x
        self.title.offset_y = y
        self.assets = []
        PicassoAsset.__init__(self, None, x, y)

    def draw(self):
        self.background.fill(BLACK)
        pygame.draw.rect(self.background, self.colour, pygame.Rect(
            self._BORDER_PIXELS, self._BORDER_PIXELS, 
            self.width - 2 * self._BORDER_PIXELS,
            self.height - 2 * self._BORDER_PIXELS,
        ))
        pygame.draw.line(self.background, BLACK, 
            (0, self._TITLE_HEIGHT_PIXELS),
            (self.width, self._TITLE_HEIGHT_PIXELS),
            self._BORDER_PIXELS,
        )
        self.background.blit(self.title.draw(), self.title.get_coordinate())
        assets = list(self.assets)
        for asset in assets:
            self.background.blit(asset.draw(), (asset.x, 
                self._TITLE_HEIGHT_PIXELS + asset.y
            ))
        return self.background

    def add_text(self, rel_x, rel_y, text, size=18):
        new_asset = TextAsset(rel_x, rel_y, text, size=size)
        self.assets.append(new_asset)
        return new_asset

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.title.offset_x = x
        self.title.offset_y = y
        
        for asset in self.assets:
            asset.offset_x = x
            asset.offset_y = y

    def finished(self):
        return True

# TODO we *might* have problems due to slider imprecesion, but should be 
# fine for smaller numbers
class BlockingSliderDialogAsset(DialogAsset):
    MAX_LENGTH = 3
    BAR_REL_BOTTOM = 60
    BAR_WIDTH_RATIO = 0.90
    SLIDER_WIDTH = 10
    SLIDER_HEIGHT = 20
    FINISHED_WIDTH = 70
    FINISHED_HEIGHT = 20
    FINISHED_REL_BOTTOM = 50

    def __init__(self, x, y, title, range_min, range_max, 
            update_callback=None, callback_args=[]):
        #self.user_input_asset = TextAsset(0, 0, '')
        DialogAsset.__init__(self, x, y, title)

        self.range_min = range_min
        self.range_max = range_max
        self.current = range_min
        self.update_callback = update_callback
        self.callback_args = callback_args

        self.bar_width = self.width * self.BAR_WIDTH_RATIO
        self.bar_start = (
            ((self.width - self.bar_width) / 2, self.height -
                self.BAR_REL_BOTTOM))

        slider_x = self.bar_start[0] - (self.SLIDER_WIDTH / 2)
        slider_y = self.bar_start[1] - (self.SLIDER_HEIGHT / 2)
        self.slider = ClickableAsset(slider_x, slider_y, 
            self.SLIDER_WIDTH, self.SLIDER_HEIGHT, "", bg_colour=BLACK, 
            highlight_bg=WHITE)
        self.slider.offset_x = self.x
        self.slider.offset_y = self.y

        button_x, button_y = self.calculate_finished_button_pos()
        self.finished_button = ClickableAsset(button_x, button_y, 
            self.FINISHED_WIDTH, self.FINISHED_HEIGHT, "DONE",
            bg_colour=BLACK, highlight_bg=WHITE, text_colour=WHITE,
            highlight_text=BLACK)
        self.finished_button.offset_x = self.x
        self.finished_button.offset_y = self.y

        self.reset()

    def draw(self):
        background = DialogAsset.draw(self)
        pygame.draw.line(
            background, BLACK,
            self.bar_start,
            (self.bar_start[0] + self.bar_width, self.bar_start[1]),
            5,
        )
        background.blit(self.slider.draw(), self.slider.get_coordinate())
        background.blit(self.finished_button.draw(), 
            self.finished_button.get_coordinate())
        if self.update_callback:
            self.update_callback(self, *self.callback_args)
        #background.blit(self.user_input_asset.draw(), (150, 150))
        return background

    def get_result(self, poll_sleep):
        done = False
        while not done:
            event = wait_for_event()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.slider.mouse_hovering(event.pos):
                    self.drag_slider(poll_sleep)
                elif self.title.mouse_hovering(event.pos):
                    self.drag_dialog(poll_sleep)
            elif event.type == pygame.MOUSEBUTTONUP and \
                    self.finished_button.mouse_hovering(event.pos):
                done = True
        return self.current

    def reset(self):
        self.user_input = '' 
        #self.user_input_asset.render_text(self.user_input)
        
    def is_numeric(self, char):
        return '0' <= char <= '9'

    def calculate_slider_rect(self):
        x = self.bar_start[0] + (self.current / self.bar_width) - \
            (self.SLIDER_WIDTH / 2)
        y = self.bar_start[1] - (self.SLIDER_HEIGHT / 2)
        return pygame.Rect(x, y, self.SLIDER_WIDTH, self.SLIDER_HEIGHT)

    def calculate_finished_button_pos(self):
        x = (self.width - self.FINISHED_WIDTH) / 2
        y = self.height - self.FINISHED_REL_BOTTOM + (self.FINISHED_HEIGHT / 2)
        return x, y

    def move_to(self, x, y):
        self.slider.offset_x = x
        self.slider.offset_y = y
        self.finished_button.offset_x = x
        self.finished_button.offset_y = y
        DialogAsset.move_to(self, x, y)

    def drag_slider(self, poll_sleep):
        base = self.bar_start[0] - (self.SLIDER_WIDTH / 2)
        interval = (self.range_max - self.range_min - 1) / self.bar_width
        while pygame.mouse.get_pressed()[0]:
            new_x = pygame.mouse.get_pos()[0] - self.x
            new_x = max(new_x, base)
            new_x = min(new_x, base + self.bar_width)
            self.slider.x = new_x
            self.slider.force_highlight = True
            self.current = self.range_min + int(((new_x - base) * interval))
            time.sleep(poll_sleep)
            pump()
        self.slider.force_highlight = False

    def drag_dialog(self, poll_sleep):
        pygame.mouse.get_rel()
        while pygame.mouse.get_pressed()[0]:
            mouse_delta = pygame.mouse.get_rel()
            new_x = max(self.x + mouse_delta[0], 0)
            new_x = min(new_x, get_picasso().get_width() - self.width)
    
            new_y = max(self.y + mouse_delta[1], 0)
            new_y = min(new_y, get_picasso().get_height() - self.height)

            self.move_to(new_x, new_y)
            time.sleep(poll_sleep)
            pump()

