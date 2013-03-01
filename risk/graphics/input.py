import time

import pygame

import risk
import risk.logger

from risk import graphics
from risk.errors.input import UserQuitInput

def handle_user_input(game_master):
    done = False
    while not done:
        done = scan_pygame_event(game_master)
        # we must yield control of program for GUI, increase to milliseconds
        # if performance gets sluggish
        time.sleep(0)

def scan_pygame_event(game_master):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise UserQuitInput()

    # TODO rewrite this mess
    for name, button in graphics.pressed_buttons():
        if name == 'next':
            return True
