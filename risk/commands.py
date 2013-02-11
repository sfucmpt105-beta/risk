import risk.logger

from risk.printer import risk_input
from risk.errors.game_master import *
from risk.errors.board import *

#Constants
_INVALID_INITIAL_INPUT = None

def help_info(player, game_master):
    print 'Available commands:'
    print '%s' % user_commands.keys()
    
def status_info(player, game_master):
    print "Player %s: " % player.name
    print '----------------------'
    print "Reserves: %s" % player.reserves
    print 'Territories:'
    territories = game_master.player_territories(player)
    for territory in territories.values():
        print '[%s]:\n' \
              'Armies: %s\n' % (territory.name, territory.armies)

def next_info(player, game_master):
    risk.logger.debug('User finished turn')
    print 'next'

def territories_info(player, game_master):
    print 'territories'
    # list of territories
	
def attack_info(player, game_master):
    print 'attack!'
	
def fortify_info(player, game_master):
    print 'fortify!'

def print_info(player, game_master):
    print 'print'

def quit_game(player, game_master):
    risk.logger.debug('User wants to quit game')
    #game_master.end_game()

user_commands = {
    'help':         help_info,           
    'status':       status_info,
    'next':         next_info,
    'territories':  territories_info,
    'attack':       attack_info,
    'fortify':      fortify_info,
    'print':        print_info,
    'quit':         quit_game,
    }

def prompt_user(player, game_master):
    user_input = _INVALID_INITIAL_INPUT
    while not user_input_finished(user_input):
        try:    # verifies that it is a valid command in the list
            user_input = risk_input('Please type a command')
            user_commands[user_input](player, game_master)  
        except KeyError:
            print 'invalid command'

def prompt_choose_territory(availables):
    print "Available territories: "
    print "---------------------------------------------------"
    print availables.keys()
    print "---------------------------------------------------"
    return risk_input('Choose from availables [empty input to reprint availables]: ')

def prompt_deploy_reserves(player, game_master, max_deploys):
    _USER_INPUT_VALID = False
    player_territories = game_master.player_territories(player)
    print "%s's territories: " % player.name
    print "---------------------------------------------------"
    print player_territories.keys()
    display_user_armies(player, player_territories)
    while not _USER_INPUT_VALID:
        try:
            user_input = risk_input(
                'Choose territory to reinforce [empty input to print' \
                'territories]: ').split()
            choice = user_input[0]
            number_of_deploys = 1
            if len(user_input) > 1:
                number_of_deploys = int(user_input[1])
            return choice, number_of_deploys
        except TypeError:
            risk.logger.error('%s is not a valid int string' % user_input[1])
        except IndexError:
            display_user_armies(player, player_territories)

def user_input_finished(user_input):
    quit_commands = ['quit', 'next']
    return user_input in quit_commands

def display_user_armies(player, player_territories):
    print "---------------------------------------------------"
    for name, territory in player_territories.iteritems():
        print "%s: %s armies" % (name, territory.armies)
    
    print "---------------------------------------------------"
    print "%s reserves left" % player.reserves
    print "---------------------------------------------------"
