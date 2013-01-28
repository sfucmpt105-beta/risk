#!/usr/bin/env python2
# std
import argparse
import sys
# user
import risk
import risk.logger
import risk.game_master
from risk import board
from risk.game_master import GameMaster

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
    game_board = board.generate_empty_board()
    return risk.game_master.GameMaster(game_board, settings)

def run_game(game_master):
    risk.logger.debug('Starting risk game...')
    game_master.choose_territories()
    while not game_master.ended:
        game_master.handle_user()
        game_master.end_turn()
    risk.logger.debug('User quit the game!') 

if __name__ == '__main__':
    settings = app_setup()
    risk.logger.debug(settings)
    master = game_setup(settings)
    run_game(master)
