#!/usr/bin/env python2
# std
import argparse
import sys
# user
import risk
import risk.logger
from risk import board

# exit codes
_EXIT_BAD_ARGS = -1

###############################################################################
## CLI option parsing
#
def app_setup():
    parser = argparse.ArgumentParser(description='Risk game with Python')
    # dev build defaults to debug for now
    parser.add_argument('--verbose', '-v', action='count',
                        help='extra output', default=risk.logger._LEVEL_DEBUG)
    settings = parser.parse_args()
    risk.logger.LOG_LEVEL = settings.verbose
    return settings


###############################################################################
## Main game functions
#
def game_setup(settings):
    return board.generate_empty_board()

def run_game(board, settings):
    print 'Game ran!'

if __name__ == '__main__':
    settings = app_setup()
    risk.logger.debug(settings)
    board = game_setup(settings)
    run_game(board, settings)
