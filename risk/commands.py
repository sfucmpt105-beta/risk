#Constants
_INVALID_INITIAL_INPUT = None

def help_info():
    print 'Available commands:'
    print '%s'%user_commands.keys()
    
def status_info():
    print 'status'
    return

def next_info():
    print 'next'
    return

def territories_info():
    print 'territories'
    return

def attack_info():
    print 'attack!'
    return

def fortify_info():
    print 'fortify!'
    return

def print_info():
    print 'print'
    return

user_commands = {
    'help':         help_info,           
    'status':       status_info,
    'next':         next_info,
    'territories':  territories_info,
    'attack':       attack_info,
    'fortify':      fortify_info,
    'print':        print_info,
    'quit':         lambda: None
    }

user_input = _INVALID_INITIAL_INPUT
while user_input != 'quit':
    try:    # verifies that it is a valid command in the list
        user_input = raw_input('Please type a command\n')
        user_commands[user_input]()  
    except KeyError:
        print 'invalid command'
