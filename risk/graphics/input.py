###############################################################################
## Input is handled by state transition diagram where mouse clicks will trigger
## state changes.
#

import time

import pygame

import risk
import risk.logger
import risk.graphics.assets.player

from risk import graphics
from risk.errors.input import UserQuitInput
from risk.errors.game_master import GameMasterError
from risk.errors.battle import RiskBattleError

from risk.graphics.event import wait_for_event, get_events
from risk.graphics.event import wait_for_mouse_click
from risk.graphics.datastore import Datastore
from risk.graphics.picasso import get_picasso
from risk.graphics.assets.player import *
from risk.graphics.assets.text import TextAsset
from risk.graphics.assets.territory import TerritoryAsset
from risk.graphics.assets.dialog import BlockingSliderDialogAsset
from risk.graphics.assets.message import PopupDialogAsset
from risk.errors.game_master import NotConnected

LAYER = '5_player_feedback'
INPUT_POLL_SLEEP = 0.01
MAX_INPUT_LENGTH = 3
DIALOG_X = 400
DIALOG_Y = 300

def slider_update(dialog, origin, target):
    datastore = Datastore()
    if not hasattr(dialog, 'show_origin_armies'):
        dialog.show_origin_armies = dialog.add_text(40, 70, 'origin')
        
    if not hasattr(dialog, 'show_target_armies'):
        dialog.show_target_armies = dialog.add_text(240, 70, 'target')

    dialog.show_origin_armies.render_text("origin: %s" % 
            (origin.armies - dialog.current))
    dialog.show_target_armies.render_text("target: %s" % dialog.current)

def get_clicked_territories(mouse_pos):
    return graphics.pressed_clickables(mouse_pos, 'territories')

def get_clicked_buttons(mouse_pos):
    return graphics.pressed_clickables(mouse_pos, 'buttons')

def handle_user_mouse_input(game_master, state_entry):
    player = game_master.current_player()
    state_entry(player, game_master)
    #wait_for_mouse_click(player, game_master, state_entry)

def get_all_clickables():
    datastore = Datastore()
    return datastore.get_storage('buttons').values() + \
           datastore.get_storage('territories').values()

def disable_all_clickables():
    for clickable in get_all_clickables():
        clickable.disabled = True

def enable_all_clickables():
    for clickable in get_all_clickables():
        clickable.disabled = False

def disable_enemy_territories(player):
    datastore = Datastore()
    for asset in datastore.get_storage('territories').values():
        if asset.territory.owner != player:
            asset.disabled = True

def enable_adjacent_territories(origin):
    datastore = Datastore()
    assets = datastore.get_storage('territories')
    assets[origin.name].disabled = False
    for neighbour in origin.neighbours.values():
        assets[neighbour.name].disabled = False

#def wait_for_mouse_click():
#    _WAITING_FOR_INPUT = True
#    
#    while _WAITING_FOR_INPUT:
#        event = wait_for_event()
#        if event.type == pygame.MOUSEBUTTONDOWN:
#            return event

def wait_for_territory_click(allow_fail=False):
    _NO_TERRITORY_CLICKED = True
    while _NO_TERRITORY_CLICKED:
        event = wait_for_mouse_click()
        for name, clickable in get_clicked_territories(event.pos):
            if isinstance(clickable, TerritoryAsset):
                return clickable
        # short circuit condition
        if allow_fail:
            return None

###############################################################################
## Reinforce phase DFA
#

def reinforce_phase(player, game_master):
    # state init vector
    datastore = Datastore()
    picasso = get_picasso()
    reserve_count_asset = ReserveCountAsset(player)
    picasso.add_asset(LAYER, reserve_count_asset)
    # core state machine
    disable_enemy_territories(player)
    while player.reserves > 0:
        event = wait_for_mouse_click()
        for name, clickable in graphics.pressed_clickables(event.pos, 
                'territories'):
            if isinstance(clickable, TerritoryAsset):
                territory = clickable.territory
                # makegonow for now, fix later
                try:
                    reinforce_add_army(player, game_master, territory)
                except GameMasterError:
                    reinforce_add_army_fail(player, game_master, territory)
    # exit state
    enable_all_clickables()
    picasso.remove_asset(LAYER, reserve_count_asset)

def reinforce_add_army(player, game_master, territory, number_of_armies=1):
    game_master.player_add_army(player, territory.name, number_of_armies)

def reinforce_add_army_fail(player, game_master, territory):
    risk.logger.debug("%s does not own %s" % (player.name, territory.name))
    dialog = PopupDialogAsset(DIALOG_X, DIALOG_Y, "Reinforce Failed!", "penis")
    get_picasso().add_asset(LAYER, dialog)
    dialog.get_confirmation()
    get_picasso().remove_asset(LAYER, dialog)

###############################################################################
## Attack phase DFA
#

def attack_phase(player, game_master):
    done = False
    while not done:
        disable_enemy_territories(player)
        event = wait_for_mouse_click()
        for name, clickable in get_clicked_territories(event.pos):
            if isinstance(clickable, TerritoryAsset):
                if clickable.territory.owner == player:
                    attack_choose_target(player, game_master, 
                            clickable)
        for name, clickable in get_clicked_buttons(event.pos):
            if name == 'next':
                done = True
    enable_all_clickables()

def attack_choose_target(player, game_master, origin_asset):
    origin = origin_asset.territory
    picasso = get_picasso()
    datastore = Datastore()
    feedback_asset = datastore.get_entry('attack_feedback')
    picasso.add_asset(LAYER, feedback_asset)
    disable_all_clickables()
    origin_asset.force_highlight = True
    enable_adjacent_territories(origin)
    target_asset = wait_for_territory_click(allow_fail=True)
    target = None
    if target_asset:
        target = target_asset.territory
    if not target:
        pass
    else:
        attack_perform_attack(player, game_master, origin, target)
    picasso.remove_asset(LAYER, feedback_asset)
    origin_asset.force_highlight = False
    enable_all_clickables()

def attack_perform_attack(player, game_master, origin, target):
    try:
        success = game_master.player_attack(player, origin.name, target.name)
        if success:
            if origin.armies > 2:
                attack_success_move_armies(player, game_master, origin, target)
            else:
                game_master.player_move_armies(player, origin.name, 
                                                target.name, 1)
        else:
            attack_failed(player, game_master, origin, target)
    except (GameMasterError, RiskBattleError, KeyError):
        pass


def attack_success_move_armies(player, game_master, origin, target):
    picasso = get_picasso()
    dialog = BlockingSliderDialogAsset(DIALOG_X, DIALOG_Y, 'Attack Move', 1, 
            origin.armies, slider_update, [origin, target])
    dialog.add_text(16, 16, "Attack was successful!")
    dialog.add_text(16, 32, "How many armies to move?")
    disable_all_clickables()
    picasso.add_asset(LAYER, dialog)
    done = False
    while not done:
        number_to_move = dialog.get_result(INPUT_POLL_SLEEP)
        try:
            game_master.player_move_armies(player, origin.name, target.name,
                    number_to_move)
            done = True
        except GameMasterError as e:
            print e
            dialog.reset()
        except ValueError:
            # we really shouldn't get a parsing error from numeric dialog
            raise 
    enable_all_clickables()
    picasso.remove_asset(LAYER, dialog)

def attack_failed(player, game_master, origin, target):
    pass

###############################################################################
## Fortify phase DFA
#

def fortify_phase(player, game_master):
    disable_enemy_territories(player)
    done = False
    # TODO merge with attack phase block
    while not done:
        event = wait_for_mouse_click()
        for name, clickable in get_clicked_territories(event.pos):
            if isinstance(clickable, TerritoryAsset):
                if clickable.territory.owner == player:
                    fortify_choose_target(player, game_master, clickable)
        for name, clickable in get_clicked_buttons(event.pos):
            if name == 'next':
                done = True
    enable_all_clickables()

def fortify_choose_target(player, game_master, origin_asset):
    origin_asset.disabled = True
    origin_asset.force_highlight = True
    origin = origin_asset.territory
    target_asset = wait_for_territory_click(allow_fail=True)
    target = None
    if target_asset:
        target = target_asset.territory
    if not target:
        # cancel
        pass
    elif target.owner == player and origin.is_connected(target):
        fortify_choose_armies_to_move(player, game_master, origin, target)
    else:
        fortify_failed(player, origin, target, 
                        TerritoryNotOwnedByPlyer(player))
    origin_asset.force_highlight = False
    origin_asset.disabled = False

def fortify_choose_armies_to_move(player, game_master, origin, target):
    picasso = get_picasso()
    dialog = BlockingSliderDialogAsset(DIALOG_X, DIALOG_Y, 'Fortify', 0, 
            origin.armies, slider_update, [origin, target])
    dialog.add_text(16, 16, "Fortifying...")
    dialog.add_text(16, 35, "Select amount of armies to move")
    disable_all_clickables()
    picasso.add_asset(LAYER, dialog)
    try:
        number_to_move = dialog.get_result(INPUT_POLL_SLEEP)
        game_master.player_move_armies(player, origin.name, 
                target.name, number_to_move)
    except GameMasterError as e:
        fortify_failed(player, origin, target, e)
    enable_all_clickables()
    picasso.remove_asset(LAYER, dialog)

def fortify_failed(player, origin, target, reason):
    picasso = get_picasso()
    expected = {
        NotConnected: 'The selected territories are not connected!',   
        TerritoryNotOwnedByPlayer: "You do not own %s!" % target.name,
    }
    msg = expected[reason.__class__] if reason.__class__ in expected.keys() \
            else "Unkonwn reason for failure..."
    dialog = PopupDialogAsset(DIALOG_X, DIALOG_Y, "Fortify Failed!", msg)
    picasso.add_asset(LAYER, dialog)
    dialog.get_confirmation()
    picasso.remove_asset(LAYER, dialog)
