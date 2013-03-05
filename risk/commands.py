import risk.logger
import risk.printer

from risk.printer import risk_input
from risk.printer import map_printer
from risk.errors.game_master import *
from risk.errors.board import *

#Constants
_INVALID_INITIAL_INPUT = None

def help_info(player, game_master):
    """
    help                            - prints help
    """
    risk.logger.debug(user_commands.keys())
    print 'Available commands:'
    for command in user_commands.values():
        if command.__doc__:
            print command.__doc__,
    print

def status_info(player, game_master):
    print "Player [%s]: " % player.name
    player_territories = game_master.player_territories(player)
    display_user_armies(player, player_territories)

def next_info(player, game_master):
    """
    next                            - ends player turn
    """
    risk.logger.debug('User finished turn')
    print 'next'

def attack_info(player, game_master, target_name, _, origin_name):
    """
    attack [target] from [origin]   - attack [target] from [origin], "from" is
                                      needed in the command
    """
    success = game_master.player_attack(player, origin_name, target_name)
    if success:
        print "successfully attacked %s!" % target_name
    else:
        print "failed to attack %s... %s reduced to 1 army" % \
            (target_name, origin_name)


def fortify_info(player, game_master, destination_territory_name, _, armies, _2, origin_territory_name):
    """
    fortify [destination] with [number] from [origin]   - fortify territory
                                    
    """
    origin_armies, destination_armies = game_master.player_move_armies(player, origin_territory_name, destination_territory_name, int(armies))
    print "%s now has: %s armies" %(origin_territory_name, origin_armies)
    print "%s now has: %s armies" %(destination_territory_name, destination_armies)
    
def print_info(player, game_master):
    print 'print'

def map_info(player, game_master, continent=None):
    """
    map                             - print ascii map for entire board
    map [continent]                 - print ascii map for continent
    """
    risk.logger.debug('printing risk map!')
    if continent:
        map_printer(continent, player, game_master)
    else:
        for continent in risk.printer.ASCII_MAPS.keys():
            map_printer(continent, player, game_master)

def add_armies(player, game_master, number_of_armies, _, territory_name):
    """ 
    add [#units] to [territory]     - add [#units] to [territory], "to" is
                                      needed in the command
    """
    armies, reserves = game_master.player_add_army(player, territory_name, int(number_of_armies))
    print "[%s] now has : [%s] units" %(territory_name, armies)
    print "[%s] unit(s) on reserve" % (player.reserves)

def quit_game(player, game_master):
    risk.logger.debug('User wants to quit game')
    #game_master.end_game()

user_commands = {
    'help':         help_info,           
    'status':       status_info,
    'next':         next_info,
    'attack':       attack_info,
    'fortify':      fortify_info,
    'print':        print_info,
    'quit':         quit_game,
    'map':          map_info,
    'add':          add_armies,
    }

reinforce_commands = {
    'help':         help_info,
    'status':       status_info,
    'map':          map_info,
    'add':          add_armies,
    'quit':         quit_game,
    }

def prompt_user(player, game_master):
    user_input = _INVALID_INITIAL_INPUT
    while not user_input_finished(user_input):
        command = None
        user_input = None
        args = None
        try:    # verifies that it is a valid command in the list
            user_input, args = risk_input('Please type a command')
            command = user_commands[user_input]
            command(player, game_master, *args)
        except KeyError:
            print 'invalid command'
        except (RiskGameError, ValueError, TypeError, IndexError) as e:
            risk.logger.error(str(e))
            if command.__doc__:
                print "usage: %s" % command.__doc__
            else:
                print command
                print user_input
                print args
                risk.logger.warn("%s syntax error and no usage. "\
                    "User input: '%s', args: '%s'" % 
                    (command, user_input, args))
            
def prompt_choose_territory(availables):
    print "Available territories: "
    print "---------------------------------------------------"
    print availables.keys()
    print "---------------------------------------------------"
    return risk_ll_input('Choose from availables [empty input to reprint availables]: ')

def prompt_deploy_reserves(player, game_master):
    _USER_INPUT_VALID = False
    player_territories = game_master.player_territories(player)
    while player.reserves > 0:
        print "%s's territories: " % player.name
        print "---------------------------------------------------"
        print player_territories.keys()
        display_user_armies(player, player_territories)
        try:
            user_input, args = risk_input('Please add all reserves to territories')
            command = reinforce_commands[user_input]
            command(player, game_master, *args)
        except KeyError:
            risk.logger.error('%s is not a valid command in the reinforcement stage' % user_input)
            risk.logger.debug(user_commands.keys())
            print 'Available commands:'
            for command in reinforce_commands.values():
                if command.__doc__:
                    print command.__doc__,
            print
        except (RiskGameError, ValueError, TypeError) as e:
            risk.logger.error(str(e))
            if command.__doc__:
                print "usage: %s" % command.__doc__
            else:
                print command
                print user_input
                print args
                risk.logger.warn("%s syntax error and no usage. "\
                    "User input: '%s', args: '%s'" % 
                    (command, user_input, args))
        except IndexError:
            print
                

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
