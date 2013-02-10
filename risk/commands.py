import risk.logger

#Constants
_INVALID_INITIAL_INPUT = None

def help_info(player, game_master, user_input):
    print 'Available commands:'
    print '%s'%user_commands.keys()
    
def status_info(player, game_master, user_input):
    print 'status'
    print 'Player %s:\n' % player 
    print 'Territories:'
    territories = game_master.player_territories(player)
    cavalries   = 0
    infantries  = 0
    artilleries = 0
    for territory in territories:
        cavalries   = territory.cavalries
        infantries  = territory.infantries
        artilleries = territory.artilleries
        print '[%s]:\n' \
        'Cavlries: %s\n' \
        'Infantries: %s\n' \
        'Artilleries: %s\n                              ' % (territory, calvaries, infantries, artilleries)

def next_info(player, game_master, user_input):
    risk.logger.debug('User finished turn')
    print 'next'

def territories_info(player, game_master, user_input):
    print 'territories'
    # list of territories
    
def attack_info(player, game_master, user_input):
    print 'attack!'
    game_master.player_attack

def attack_help(player, game_master, user_input):
    print 'To attack a player type:\n' \
        '\"attack [territory_origin] [territory_target]\"\n'
    
def fortify_info(player, game_master, user_input):
    print 'fortify!'
    

def fortify_help(player, game_master, user_input):
    print 'To use fortify type:\n' \
    '\"fortify [territory_origin] [territory_destination] [type] [#]\"\n' \
    '[type] of unit please enter:\n' \
    'i = infantry\n' \
    'c = cavalry\n' \
    'a = artilery\n'
    
def print_info(player, game_master, user_input):
    print 'print'

def add_unit(player, game_master, user_input):
    user_input = user_input
    if user_input == 'add infantry':
        #game_master.player_add_infantry
        print 'Adding infantry'

    if user_input == 'add cavalry':
        #game_master.player_add_cavalry
        print 'Adding cavalry'
    
    if user_input == 'add artilery':
        #game_master.player_add_artilery
        print 'Adding artilery'
    
def quit_game(player, game_master, user_input):
    risk.logger.debug('User wants to quit game')
    game_master.end_game()

user_commands = {
    'help':         help_info,
    'help fortify': fortify_help,
    'help attack':  attack_help,
    'status':       status_info,
    'next':         next_info,
    'territories':  territories_info,
    'attack':       attack_info,
    'fortify':      fortify_info,
    'print':        print_info,
    'add infantry': add_unit,
    'add cavalry':  add_unit,
    'add artilery,':add_unit,
    'quit':         quit_game,
    }

def prompt_user(player, game_master):
    user_input = _INVALID_INITIAL_INPUT
    while not user_input_finished(user_input):
        try:    # verifies that it is a valid command in the list
            user_input = raw_input('[Please type a command]: ')
            user_commands[user_input](player, game_master, user_input)  
        except KeyError:
            print 'invalid command'

def user_input_finished(user_input):
    quit_commands = ['quit', 'next']
    return user_input in quit_commands
