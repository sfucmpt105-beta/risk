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
import risk.graphics.assets.dialog
import risk.graphics.assets.image
import risk.graphics.assets.gameplay

from risk.logger import *
from risk.game_master import UNDEFINED, REINFORCE, ATTACK, FORTIFY
from risk.graphics import assets
from risk.graphics.event import wait_for_event, get_events
from risk.graphics.datastore import Datastore
from risk.graphics.picasso import get_picasso
from risk.graphics.assets.territory import build_territory_asset
from risk.graphics.assets.territory import build_player_colour_mapping
from risk.graphics.assets.territory import TerritoryAsset

DEFAULT_WIDTH  = 1152
DEFAULT_HEIGHT = 720
DEFAULT_BACKGROUND = 'resources/risk_board.png'
DEFAULT_OVERLAY = 'assets/art/gui/main_borders.png'

INFO_PANEL_X = 370
INFO_PANEL_Y = 585
INFO_PANEL_WIDTH = 410
INFO_PANEL_HEIGHT = 110

territory_coordinates = {
    'north_america': {
        'alaska': (29, 117),
        'northwest_territory': (98, 97),
        'greenland': (335, 42),
        'alberta': (113, 157),
        'ontario': (227, 158),
        'eastern_canada': (310, 153),
        'western_united_states': (164, 213),
        'eastern_united_states': (245, 210),
        'central_america': (182, 267)
    },
    'south_america': {
        'venezuela': (293, 328),
        'peru': (291, 372),
        'brazil': (344, 350),
        'argentina': (317, 445),
    },
    'europe': {
        'iceland': (517, 122),
        'scandinavia': (577, 113),
        'russia': (630, 119),
        'great_britain': (511, 166),
        'northern_europe': (576, 177),
        'western_europe': (528, 200),
        'southern_europe': (589, 211)
    },
    'africa': {
        'north_africa': (504, 251),
        'egypt': (603, 253),
        'central_africa': (581, 333),
        'east_africa': (651, 302),
        'south_africa': (601, 395),
        'madagascar': (698, 380)
    },
    'asia': {
        'ural': (764, 92),
        'siberia': (793, 57),
        'yakutsk': (930, 90),
        'kamchatka': (983, 115),
        'irkutsk': (875, 142),
        'afghanistan': (705, 192),
        'china': (811, 196),
        'mongolia': (871, 182),
        'japan': (977, 201),
        'middle_east': (644, 230),
        'india': (770, 257),
        'southern_asia': (847, 274)
    },
    'australia': {
        'indonesia': (861, 355),
        'new_guinea': (994, 357),
        'western_australia': (941, 412),
        'eastern_australia': (1004, 402)
    }
}

def init(game_master):
    debug("initializing graphics library...")
    add_graphic_hooks(game_master)
    debug("attempting to get singleton picasso")
    picasso = risk.graphics.picasso.get_picasso(width=DEFAULT_WIDTH, 
            height=DEFAULT_HEIGHT, background=DEFAULT_BACKGROUND)
    debug("obtained picasso instance")
    debug("building risk board")
    initialize_territories(picasso, game_master)
    initialize_other_graphic_assets(picasso, game_master)
    debug("starting picasso graphics subsystem")
    picasso.start()
    debug("picasso subsystem successfully launched!")
    debug("adding basic assets")
    add_overlay(picasso)
    add_buttons(picasso)
    debug("returning control to main loop")

def shutdown(*args):
    debug("end game event received! attempting to shutdown picasso...")
    picasso = risk.graphics.picasso.get_picasso()
    picasso.end()
    debug("sent picasso shutdown event, fingers crossed...")

def add_graphic_hooks(game_master):
    game_master.add_start_turn_callback(check_picasso_liveness)
    game_master.add_start_turn_callback(show_bot_player_hint)
    #game_master.add_start_turn_callback(show_human_player)
    game_master.add_start_turn_callback(delay)
    game_master.add_start_turn_callback(check_gui_quit_event)
    game_master.add_end_turn_callback(check_gui_quit_event)
    game_master.add_end_action_callback(release_control)
    game_master.add_start_turn_callback(update_game_info_panel)
    game_master.add_end_action_callback(update_game_info_panel)
    game_master.add_end_phase_callback(update_current_phase)
    game_master.add_start_turn_callback(show_current_human_player)
    #game_master.add_end_action_callback(delay)

def initialize_territories(picasso, game_master):
    datastore = Datastore()
    for continent, territories in game_master.board.continents.iteritems():
        for territory_name, territory in territories.iteritems():
            coordinate = territory_coordinates[continent][territory_name]
            graphic_asset = build_territory_asset(continent, territory, coordinate[0], coordinate[1])
            army_count_asset = assets.territory.ArmyCountAsset(graphic_asset)
            picasso.add_asset('3_territories', graphic_asset)
            picasso.add_asset('4_army_count', army_count_asset)
            
            datastore.add_entry(territory_name, graphic_asset, 'territories')
    risk.logger.debug("assigning player colours")
    build_player_colour_mapping(game_master.players)

def initialize_other_graphic_assets(picasso, game_master):
    picasso = get_picasso()
    datastore = Datastore()
    #current_player_asset = assets.text.CurrentPlayerAsset(
    #        100, 100, game_master)
    #picasso.add_asset('4_current_player', current_player_asset)
    #datastore.add_entry('current_player', current_player_asset)
    feedback_asset = assets.text.TextAsset(100, 650, 
            'choose territory to attack')
    datastore.add_entry('attack_feedback', feedback_asset)
    game_info_asset = assets.gameplay.PlayersAsset(30, 550, game_master)
    picasso.add_asset('999_ontop', game_info_asset)
    datastore.add_entry('game_info', game_info_asset)
    add_state_indicators(picasso, game_master)
    player_background_asset = assets.base.ColourBlockAsset(
        1000, 548, 123, 80, assets.base.BLACK)
    human_player_asset = assets.base.ColourBlockAsset(
        1002, 550, 119, 76, assets.base.GREY)
    datastore.add_entry('player_colour', human_player_asset)
    picasso.add_asset('999_ontop', player_background_asset)
    picasso.add_asset('999_ontop1', human_player_asset)

def add_state_indicators(picasso, game_master):
    datastore = Datastore()
    pos_x = 867
    state_indicators = {
        'reinforce': (pos_x, 548),
        'attack': (pos_x, 600),
        'fortify': (pos_x, 652),
    }
    for state, coordinate in state_indicators.iteritems():
        asset = assets.image.ToggleImageAsset(coordinate[0], coordinate[1],
            "assets/art/gui/button_%s_highlight.png" % state)
        datastore.add_entry(state, asset, 'states')
        picasso.add_asset('999_ontop', asset)
   
def add_buttons(picasso):
    datastore = Datastore()
    #next_button = assets.clickable.ClickableAsset(
    #    1000, 635, 120, 65, 'NEXT')
    next_button = assets.clickable.ImageButtonAsset(
        1000, 635,
        'assets/art/gui/button_next_up.png',
        'assets/art/gui/button_next_down.png'
    )
    datastore.add_entry('next', next_button, 'buttons')

    for button in datastore.get_storage('buttons').values():
        picasso.add_asset('1_buttons', button)

def add_overlay(picasso):
    datastore = Datastore()
    overlay = assets.image.ImageAsset(0, 0, DEFAULT_OVERLAY)
    datastore.add_entry('overlay', overlay)
    picasso.add_asset('0_overlay', overlay)

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

def show_current_human_player(game_master):
    datastore = Datastore()
    asset = datastore.get_entry('player_colour')
    player = game_master.current_player()
    if isinstance(player, risk.player.HumonRiskPlayer):
        try:
            asset.set_colour(TerritoryAsset.mapping[player])
        except KeyError:
            error("couldn't find key entry for player: %s" % player.name)
            asset.set_colour(assets.base.BLACK)
    else:
        asset.set_colour(assets.base.GREY)

def is_human_player(game_master):
    return isinstance(game_master.current_player(), 
            risk.player.HumonRiskPlayer)

def delay(game_master, *args):
    if not is_human_player(game_master):
        time.sleep(1)

def check_picasso_liveness(game_master):
    if not get_picasso().is_alive():
        game_master.end_game()

def check_gui_quit_event(game_master):
    if not is_human_player(game_master):
        for event in get_events():
            if event.type == pygame.QUIT:
                game_master.end_game()

def update_game_info_panel(*args):
    Datastore().get_entry('game_info').update()

def update_current_phase(game_master, previous, current):
    for state, asset in Datastore().get_storage('states').iteritems():
        asset.set_state(state == current)

def show_bot_player_hint(game_master):
    datastore = Datastore()
    picasso = get_picasso()
    if not datastore.has_entry('bot_player_hint'):
        hint_asset = assets.text.CentredTextAsset(INFO_PANEL_X, INFO_PANEL_Y, 
                    INFO_PANEL_WIDTH, INFO_PANEL_HEIGHT, 
                    "AI TAKING TURNS...",
                    bold=True)
        datastore.add_entry('bot_player_hint', hint_asset)
    hint_asset = datastore.get_entry('bot_player_hint')
    if isinstance(game_master.current_player(), risk.ai.bots.BasicRiskBot):
        picasso.add_asset('999', hint_asset)
    else:
        picasso.remove_asset('999', hint_asset)

def release_control(game_master, *args):
    # release CPU for faster screen update
    time.sleep(0)

def pressed_clickables(mouse_pos, storage='buttons'):
    datastore = Datastore()
    storage = datastore.get_storage(storage)
    clicked = []
    for name, button in storage.iteritems():
        if button.mouse_hovering(mouse_pos):
            if button.confirmed_click():
                clicked.append((name, button))
    return clicked
