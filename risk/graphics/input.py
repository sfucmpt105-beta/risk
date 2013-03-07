import time

import pygame

import risk
import risk.logger
import risk.graphics.assets.player

from risk import graphics
from risk.errors.input import UserQuitInput
from risk.errors.game_master import GameMasterError
from risk.errors.battle import RiskBattleError

from risk.graphics.datastore import Datastore
from risk.graphics.picasso import get_picasso
from risk.graphics.assets.player import *
from risk.graphics.assets.territory import TerritoryAsset

LAYER = '5_player_feedback'
INPUT_POLL_SLEEP = 0.1

def get_clicked_territories(mouse_pos):
    return graphics.pressed_clickables(mouse_pos, 'territories')

def get_clicked_buttons(mouse_pos):
    return graphics.pressed_clickables(mouse_pos, 'buttons')

def handle_user_input(game_master):
    done = False
    player = game_master.current_player()
    picasso = get_picasso()
    reserve_count_asset = ReserveCountAsset(player)
    picasso.add_asset(LAYER, reserve_count_asset)
    scan_pygame_event(player, game_master, reinforce_phase)
        # we must yield control of program for GUI, increase to milliseconds
        # if performance gets sluggish
    picasso.remove_asset(LAYER, reserve_count_asset)
    scan_pygame_event(player, game_master, attack_phase)
    

def scan_pygame_event(player, game_master, click_callback):
    result = None
    while not result:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise UserQuitInput()
            elif event.type == pygame.MOUSEBUTTONUP:
                result = click_callback(player, game_master, event)
        time.sleep(INPUT_POLL_SLEEP)
    return result

def reinforce_phase(player, game_master, event):
    datastore = Datastore()
    for name, clickable in graphics.pressed_clickables(event.pos, 
            'territories'):
        if isinstance(clickable, TerritoryAsset):
            territory = clickable.territory
            # makegonow for now, fix later
            try:
                game_master.player_add_army(player, territory.name)
            except GameMasterError:
                pass
    if player.reserves <= 0:
        return True
    else:
        return False

def attack_phase(player, game_master, event):
    for name, clickable in get_clicked_territories(event.pos):
        if isinstance(clickable, TerritoryAsset):
            if clickable.territory.owner == player:
                attacking_mode(player, game_master, clickable.territory)
    for name, clickable in get_clicked_buttons(event.pos):
        if name == 'next':
            return True

def attacking_mode(player, game_master, origin):
    picasso = get_picasso()
    datastore = Datastore()
    feedback_asset = datastore.get_entry('attack_feedback')
    picasso.add_asset(LAYER, feedback_asset)
    target = scan_pygame_event(player, game_master, choose_target)
    try:
        game_master.player_attack(player, origin.name, target.name)
    except (GameMasterError, RiskBattleError, KeyError):
        pass
    finally:
        picasso.remove_asset(LAYER, feedback_asset)


def choose_target(player, game_master, event):
    for name, clickable in get_clicked_territories(event.pos):
        if isinstance(clickable, TerritoryAsset):
            return clickable.territory
