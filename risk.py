#!/usr/bin/env python2
# adding some useless comment
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
                        help='extra output', default=risk.logger.LEVEL_DEBUG)
    settings = parser.parse_args()
    risk.logger.LOG_LEVEL = settings.verbose
    return settings


###############################################################################
## Debug functions
#
def end_turn_debug_print(game_master):
    risk.logger.debug('Ending turn...')

###############################################################################
## Main game functions
#
def game_setup(settings):
    _DEV_HUMAN_PLAYERS = 6
    game_board = board.generate_empty_board()
    game_master = risk.game_master.GameMaster(game_board, settings)
    game_master.generate_human_players(_DEV_HUMAN_PLAYERS)
    game_master.add_end_turn_callback(end_turn_debug_print)
    return game_master

def run_game(game_master):
    risk.logger.debug('Starting risk game...')
    game_master.choose_territories()
    player = 0
    while not game_master.ended:
        game_master.player_take_turn(player)
        game_master.call_end_turn_callbacks()
        player = (player + 1) % game_master.number_of_players()
    risk.logger.debug('User quit the game!') 

if __name__ == '__main__':
    settings = app_setup()
    risk.logger.debug(settings)
    master = game_setup(settings)
    run_game(master)
