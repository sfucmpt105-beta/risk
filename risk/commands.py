import risk.logger

from risk.printer import risk_input

#Constants
_INVALID_INITIAL_INPUT = None

def help_info(player, game_master):
    print 'Available commands:'
    print '%s'%user_commands.keys()
    
def status_info(player, game_master):
    print 'Player %s:\n' % player.name
    print '----------------------'
    print 'Territories:'
    territories = game_master.player_territories(player)
    for territory in territories:
        print '[%s]:\n' \
              'Cavlries: %s\n' \
              'Infantries: %s\n' \
              'Artilleries: %s\n' % (territory, territory.armies)

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
    game_master.end_game()

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

def user_input_finished(user_input):
    quit_commands = ['quit', 'next']
    return user_input in quit_commands
