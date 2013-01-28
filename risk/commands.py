import risk.logger

#Constants
_INVALID_INITIAL_INPUT = None

def help_info(game_master):
    print 'Available commands:'
    print '%s'%user_commands.keys()
    
def status_info(game_master):
    print 'status'

def next_info(game_master):
    risk.logger.debug('User finished turn')
    print 'next'

def territories_info(game_master):
    print 'territories'

def attack_info(game_master):
    print 'attack!'

def fortify_info(game_master):
    print 'fortify!'

def print_info(game_master):
    print 'print'

def quit_game(game_master):
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

def prompt_user(game_master):
    user_input = _INVALID_INITIAL_INPUT
    while not user_input_finished(user_input):
        try:    # verifies that it is a valid command in the list
            user_input = raw_input('[Please type a command]: ')
            user_commands[user_input](game_master)  
        except KeyError:
            print 'invalid command'

def user_input_finished(user_input):
    quit_commands = ['quit', 'next']
    return user_input in quit_commands
