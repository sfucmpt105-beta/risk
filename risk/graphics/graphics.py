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
from risk.graphics.datastore import Datastore
from risk.graphics.picasso import get_picasso
from risk.graphics.assets.territory import build_territory_asset
from risk.graphics.assets.territory import build_player_colour_mapping

DEFAULT_WIDTH  = 1152
DEFAULT_HEIGHT = 720
DEFAULT_BACKGROUND = 'resources/risk_board.png'

buttons = {}

territory_coordinates = {
    'north_america': {
        'alaska': (80, 171),
        'northwest_territory': (201, 143),
        'greenland': (428, 118),
        'alberta': (168, 199),
        'ontario': (278,210 ),
        'eastern_canada': (353, 207),
        'western_united_states': (213, 256),
        'eastern_united_states': (301, 262),
        'central_america': (251, 316)
    },
    'south_america': {
        'venezuela': (356, 369),
        'peru': (345, 428),
        'brazil': (416, 419),
        'argentina': (361, 506),
    },
    'europe': {
        'iceland': (545, 150),
        'scandinavia': (629, 166),
        'russia': (711, 198),
        'great_britain': (539, 201),
        'northern_europe': (624, 213),
        'western_europe': (568, 243),
        'southern_europe': (638, 248)
    },
    'africa': {
        'north_africa': (585, 320),
        'egypt': (644, 299),
        'central_africa': (638, 380),
        'east_africa': (695, 373),
        'south_africa': (651, 436),
        'madagascar': (752, 432)
    },
    'asia': {
        'ural': (818, 182),
        'siberia': (878, 166),
        'yakutsk': (986, 152),
        'kamchatka': (1062, 175),
        'irkutsk': (936, 195),
        'afghanistan': (769, 249),
        'china': (883, 266),
        'mongolia': (930, 243),
        'japan': (1044, 274),
        'middle_east': (718, 295),
        'india': (822, 310),
        'southern_asia': (884, 330)
    },
    'australia': {
        'indonesia': (922, 413),
        'new_guinea': (1040, 402),
        'western_australia': (995, 474),
        'eastern_australia': (1055, 467)
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
    datastore = Datastore()
    current_player_asset = assets.text.CurrentPlayerAsset(
            100, 100, game_master)
    picasso.add_asset('4_current_player', current_player_asset)
    datastore.add_entry('current_player', current_player_asset)
    feedback_asset = assets.text.TextAsset(100, 650, 
            'choose territory to attack')
    datastore.add_entry('attack_feedback', feedback_asset)
    
def add_buttons(picasso):
    datastore = Datastore()
    next_button = assets.clickable.ClickableAsset(
        100, 500, 100, 100, 'NEXT')
    datastore.add_entry('next', next_button, 'buttons')

    for button in datastore.get_storage('buttons').values():
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

def pressed_clickables(mouse_pos, storage='buttons'):
    datastore = Datastore()
    storage = datastore.get_storage(storage)
    clicked = []
    for name, button in storage.iteritems():
        if button.mouse_hovering(mouse_pos):
            clicked.append((name, button))
    return clicked
