import re

import risk.errors.input

FORMAT="[%s: %s] >>> "

def risk_input(msg, stage="RISK"):
    user_input = raw_input(FORMAT % (stage, msg))
    if user_input == 'quit':
        raise risk.errors.input.UserQuitInput()
    else:
        return user_input

def map_printer(continent, player, game_master):
    ascii_map = ASCII_MAPS[continent]
    # regex magic... sigh :(
    continent = game_master.board.continents[continent]
    for name, territory in continent.iteritems():
        symbol = SYMBOL_MAPPING[name]
        ascii_map = re.sub(
            "!%s" % symbol, "%02d" % territory.armies, ascii_map)
        if territory.owner == player:
            ascii_map = re.sub(symbol, '*', ascii_map)
        else:
            ascii_map = re.sub(symbol, '.', ascii_map)
    print ascii_map
        

ASCII_MAPS = {
    'north_america' :
r"""
    =======================================================================
    ||                                                                   ||
    ~~  AAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBB   EEEEEEEEEEEEEE               ~~
    ~~  A alaska AB northwest_territory B---E  greenland E               ~~
    ||  A   !A   AB         !B          B   E     !E     E-\__[europe]   ||
    ||  AAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBB   EEEEEEEEEEEEEE    iceland => ||
    ~~   CCCCCCCCCCCDDDDDDDDDDD                /    |                    ~~
    ~~   C alberta CD ontario D----------------     |                    ~~
    ||   C   !C    CD   !D    D         FFFFFFFFFFFFFFFFFF               ||
    ||   CCCCCCCCCCCDDDDDDDDDDD---------F eastern_canada F               ||
    ~~        |          |   \          F       !F       F               ~~
    ~~        |          |    \         FFFFFFFFFFFFFFFFFF               ~~
    ||        |          |     ------ |                                  ||
    ||   GGGGGGGGGGGGGGGGGGGGGGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHH            ||
    ~~   G western_united_states GH eastern_united_states   H            ~~
    ~~   G         !G            GH         !H              H            ~~
    ||   GGGGGGGGGGGGGGGGGGGGGGGGGHHHHHHHHHHHHHHHHHHHHHHHHHHH            ||
    ||           IIIIIIIIIIIIIIIIIII                                     ||
    ~~           I central_america I                                     ~~
    ~~           I       !I        I                                     ~~
    ||           IIIIIIIIIIIIIIIIIII                                     ||
    ||                  \                                               ||
    ~~               [south_america]                                     ~~
    ~~                  venezuela                                        ~~
    ||                     |                                            ||
    ||                     \/                                            ||
    ~~                                                                   ~~
    =======================================================================
""",
    'europe': ""
}

SYMBOL_MAPPING = {
    # North America
    'alaska' : 'A',
    'northwest_territory': 'B',
    'alberta': 'C',
    'ontario': 'D',
    'greenland': 'E',
    'eastern_canada': 'F',
    'western_united_states': 'G',
    'eastern_united_states': 'H',
    'central_america': 'I',
    # Central America
    'venezuela': 'A',
    'brazil': 'B',
    'peru': 'C',
    'argentina': 'D',
    # Africa
    'north_africa': 'A',
    'egypt': 'B',
    'east_africa': 'C',
    'central_africa': 'D',
    'south_africa': 'E',
    'madagascar': 'F',
    # Europe
    'iceland': 'A',
    'great_britain': 'B',
    'western_europe': 'C',
    'northern_europe': 'D',
    'southern_europe': 'E',
    'scandinavia': 'F',
    'russia': 'G',
    # Asia
    'kamchatka': 'A',
    'yakutsk': 'B',
    'siberia': 'C',
    'ural': 'D',
    'afghanistan': 'E',
    'middle_east': 'F',
    'india': 'G',
    'southern_asia': 'H',
    'china': 'I',
    'mongolia': 'J',
    'irkutsk': 'K',
    'japan': 'L',
    # Australia
    'indonesia': 'A',
    'new_guinea': 'B',
    'western_australia': 'C',
    'eastern_australia': 'D',
}
