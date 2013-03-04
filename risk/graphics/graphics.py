import thread
import time

import pygame

import risk
import risk.player
import risk.graphics
import risk.graphics.picasso
import risk.graphics.assets.text
import risk.graphics.assets.clickable
import risk.graphics.assets.territory
from risk.logger import *
from risk.graphics import assets
from risk.graphics.picasso import get_picasso
from risk.graphics.assets.territory import build_territory_asset
from risk.graphics.assets.territory import build_player_colour_mapping

DEFAULT_WIDTH  = 1152
DEFAULT_HEIGHT = 720
DEFAULT_BACKGROUND = 'resources/risk_board.png'

buttons = {}

def init(game_master):
    print assets
    debug("initializing graphics library...")
    add_graphic_hooks(game_master)
    debug("attempting to get singleton picasso")
    picasso = risk.graphics.picasso.get_picasso(width=DEFAULT_WIDTH, 
            height=DEFAULT_HEIGHT, background=DEFAULT_BACKGROUND)
    debug("obtained picasso instance")
    debug("building risk board")
    initialize_territories(picasso, game_master)
    debug("starting picasso graphics subsystem")
    picasso.start()
    debug("picasso subsystem successfully launched!")
    debug("adding basic assets")
    add_buttons(picasso)
    debug("returning control to main loop")

def shutdown(*args):
    debug("end game event received! attempting to shutdown picasso...")
    picasso = risk.graphics.picasso.get_picasso()
    picasso.end()
    debug("sent picasso shutdown event, fingers crossed...")

def add_graphic_hooks(game_master):
    game_master.add_start_turn_callback(check_picasso_liveness)
    game_master.add_start_turn_callback(show_human_player)
    game_master.add_start_turn_callback(delay)
    game_master.add_start_turn_callback(check_gui_quit_event)
    game_master.add_end_turn_callback(check_gui_quit_event)
    game_master.add_end_action_callback(release_control)

def initialize_territories(picasso, game_master):
    territory = game_master.board['alaska']
    asset = build_territory_asset('north_america', territory, 64, 80)
    picasso.add_asset('3_territories', asset)
    territory = game_master.board['central_america']
    asset = build_territory_asset('north_america', territory, 150, 300)
    picasso.add_asset('3_territories', asset)
    risk.logger.debug("assigning player colours")
    build_player_colour_mapping(game_master.players)

def add_buttons(picasso):
    global buttons
    # TODO GET RID OF
    next_button = assets.clickable.ClickableAsset(
        100, 500, 100, 100, 'NEXT')
    buttons['next'] = next_button

    for button in buttons.values():
        picasso.add_asset('1_buttons', button)

def show_human_player(game_master):
    layer = 3
    if not hasattr(show_human_player, 'asset'):
        asset = assets.text.TextAsset(
            50, 50, 'Player is taking turn...')
        setattr(show_human_player, 'asset', asset)
    asset = getattr(show_human_player, 'asset')
    if isinstance(game_master.current_player(), risk.player.HumonRiskPlayer):
        get_picasso().add_asset('1_text', asset)
    else:
        get_picasso().remove_asset('1_text', asset)

def is_human_player(game_master):
    return isinstance(game_master.current_player(), 
            risk.player.HumonRiskPlayer)

def delay(game_master):
    if not is_human_player(game_master):
        time.sleep(1)

def check_picasso_liveness(game_master):
    if not get_picasso().is_alive():
        game_master.end_game()

def check_gui_quit_event(game_master):
    if not is_human_player(game_master):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_master.end_game()

def release_control(game_master, *args):
    # release CPU for faster screen update
    time.sleep(0)

def pressed_buttons():
    clicked = []
    for name, button in buttons.iteritems():
        if button.clicked():
            clicked.append((name, button))
    return clicked
