import thread

import risk
import risk.graphics.picasso
from risk.logger import *

DEFAULT_WIDTH  = 1152
DEFAULT_HEIGHT = 720
DEFAULT_BACKGROUND = 'resources/risk_board.png'

def init():
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
