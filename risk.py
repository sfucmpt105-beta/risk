#!/usr/bin/env python2
# std
import argparse
import sys
import os
# user
import risk
import risk.logger
import risk.game_master
from risk import board
from risk.game_master import GameMaster

# fixes the pathing so that the game doesn't need to be run from root
if '__file__' in globals():
    root = os.path.dirname(__file__) or './'
    os.path.join(root)
    os.chdir(root)

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
    parser.add_argument('--cli', '-c', action='store_true',
                        help='commandline version of game', default=False)
    settings = parser.parse_args()
    risk.logger.LOG_LEVEL = settings.verbose
    return settings

###############################################################################
## CLI functionsr
#
def print_banner():
    print \
"""
    --==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==--
    ||                              PyRisk                             ||
    ||-----------------------------------------------------------------||
    || Risk is a turn-based game for two to six players. The standard  ||
    || version is played on a board depicting a political map of the   ||
    || Earth, divided into forty-two territories, which are grouped    ||
    || into six continents. The primary object of the game is "world   ||
    || domination," or "to occupy every territory on the board and in  ||
    || so doing, eliminate all other players." Players control         ||
    || armies with which they attempt to capture territories from      ||
    || other players, with results determined by dice rolls.           ||
    ||-----------------------------------------------------------------||
    ||                     By: CMPT106 Group Beta                      ||
    --==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==-==--
"""


###############################################################################
## Debug functions
#
def end_turn_debug_print(game_master):
    risk.logger.debug('Ending turn...')

###############################################################################
## Main game functions
#
def game_setup(settings):
    _DEV_HUMAN_PLAYERS = 1
    game_board = board.generate_empty_board()
    #game_board = board.generate_mini_board()
    game_master = risk.game_master.GameMaster(game_board, settings)
    game_master.generate_players(_DEV_HUMAN_PLAYERS, settings.cli)
    game_master.add_end_turn_callback(end_turn_debug_print)
    # dev
    board.dev_random_assign_owners(game_master)
    return game_master

def run_game(game_master):
    print_banner()
    risk.logger.debug('Starting risk game...')
    try:
        #game_master.choose_territories()
        #game_master.deploy_troops()
        while not game_master.ended:
            run_turn(game_master)
    except (risk.errors.input.UserQuitInput, KeyboardInterrupt, EOFError):
        game_master.end_game()
    except BaseException as e:
        risk.logger.critical(repr(e))
        risk.logger.critical('unknown error occured, attempting perform'\
            ' graceful shutdown...')
        game_master.end_game()
    risk.logger.debug('User quit the game!')

def run_turn(game_master):
    risk.logger.debug('Current player is: %s' % 
                      game_master.current_player().name)
    game_master.player_take_turn()
    game_master.call_end_turn_callbacks()
    game_master.end_turn()

if __name__ == '__main__':
    settings = app_setup()
    risk.logger.debug(settings)
    master = game_setup(settings)
    if not settings.cli:
        import risk.graphics
        risk.graphics.init(master)
        master.add_end_game_callback(risk.graphics.shutdown)
    run_game(master)
