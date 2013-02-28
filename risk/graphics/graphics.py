import thread
import time

import risk
import risk.player
import risk.graphics
import risk.graphics.picasso
import risk.graphics.assets.text
from risk.logger import *
from risk.graphics import assets
from risk.graphics.picasso import get_picasso

DEFAULT_WIDTH  = 1152
DEFAULT_HEIGHT = 720
DEFAULT_BACKGROUND = 'resources/risk_board.png'

def init(game_master):
    print assets
    add_graphic_hooks(game_master)
    debug("initializing graphics library...")
    debug("attempting to get singleton picasso")
    picasso = risk.graphics.picasso.get_picasso(width=DEFAULT_WIDTH, 
            height=DEFAULT_HEIGHT, background=DEFAULT_BACKGROUND)
    debug("obtained picasso instance")
    debug("starting picasso graphics subsystem")
    picasso.start()
    debug("picasso subsystem successfully launched!")
    debug("returning control to main loop")

def shutdown(*args):
    debug("end game event received! attempting to shutdown picasso...")
    picasso = risk.graphics.picasso.get_picasso()
    picasso.end()
    debug("sent picasso shutdown event, fingers crossed...")

def add_graphic_hooks(game_master):
    game_master.add_start_turn_callback(show_human_player)
    game_master.add_start_turn_callback(delay)

def show_human_player(game_master):
    layer = 3
    if not hasattr(show_human_player, 'asset'):
        asset = assets.text.TextAsset(
            'Player is taking turn...', 50, 50)
        setattr(show_human_player, 'asset', asset)
    asset = getattr(show_human_player, 'asset')
    if isinstance(game_master.current_player(), risk.player.HumonRiskPlayer):
        get_picasso().add_asset('1_text', asset)
    else:
        get_picasso().remove_asset('1_text', asset)

def delay(game_master):
    if not isinstance(game_master.current_player(), risk.player.HumonRiskPlayer):
        time.sleep(1)
