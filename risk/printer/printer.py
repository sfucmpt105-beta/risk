import re

import risk.errors.input

FORMAT="[%s: %s] >>> "

def risk_ll_input(msg, stage="RISK"):
    """
    low-level input handler
    """
    user_input = raw_input(FORMAT % (stage, msg))
    if user_input == 'quit':
        raise risk.errors.input.UserQuitInput()
    else:
        return user_input

def risk_input(msg, stage="RISK"):
    user_input = risk_ll_input(msg, stage)
    processed = user_input.split()
    command = processed[0]
    args = processed[1:]
    return command, args

def map_printer(continent_name, player, game_master):
    ascii_map = ASCII_MAPS[continent_name]
    # regex magic... sigh :(
    continent = game_master.board.continents[continent_name]
    for name, territory in continent.iteritems():
        symbol = SYMBOL_MAPPING[name]
        ascii_map = re.sub(
            "!%s" % symbol, "%02d" % territory.armies, ascii_map)
        if territory.owner == player:
            ascii_map = re.sub(symbol, '*', ascii_map)
        else:
            ascii_map = re.sub(symbol, '\'', ascii_map)
    print continent_name
    print '-' * len(continent_name),
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
    ||                   IIIIIIIIIIIIIIIIIII                             ||
    ~~                   I central_america I                             ~~
    ~~                   I       !I        I                             ~~
    ||                   IIIIIIIIIIIIIIIIIII                             ||
    ||                          \                                        ||
    ~~                       [south_america]                             ~~
    ~~                          venezuela                                ~~
    ||                             |                                     ||
    ||                             \/                                    ||
    ~~                                                                   ~~
    =======================================================================
""",
    'europe': 
r"""
    =======================================================================
    ||                                                                   ||
    ~~ [north_america]  AAAAAAAAAAA      FFFFFFFFFFFFFFFGGGGGGGGGG       ~~      
    ~~ <==== greenland--A iceland A------F scandinavia FG        G       ~~
    ||                  A   !A    A     /F     !F      FG russia G       ||
    ||                  AAAAAAAAAAA    / FFFFFFFFFFFFFFFG   !G   G       ||
    ~~                      |         /         |       G        G       ~~
    ~~               BBBBBBBBBBBBBBBBB          |       G       G        ~~
    ||               B great_britain B          |       G      G [asia]  ||
    ||               B      !B       B          |       G     G--ural => ||
    ~~               BBBBBBBBBBBBBBBBB          |       G    G           ~~
    ~~                        \                 |       G   G            ~~
    || CCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDG  G            ||
    || C western_europe  CD        northern_europe      DG  G            ||
    ~~ C                 CD              !D             DG  G            ~~
    ~~ C                 CDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDG  G            ~~
    || C                 CEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEG  G             ||
    || C                 CE       southern_europe    E G  G   [asia]     ||
    ~~ C                 CE            !E            EG  G-afghanistan =>~~
    ~~ CCCCCCCCCCCCCCCCCCCEEEEEEEEEEEEEEEEEEEEEEEEEEEEGGGG               ~~
    ||         |                        |                 \              ||
    ||      [africa]                 [africa]              \ [asia]      ||
    ~~    north_africa                egypt               middle_east => ~~       
    ~~         |                         |                               ~~
    ||         \/                        \/                              ||
    =======================================================================
""",
    'africa':
r"""
    =======================================================================
    ||                                                                   ||
    ~~                        /\               /\                        ~~
    ~~                        |                |                         ~~
    ||                      [europe]        [europe]                     ||
    ||                    western_europe  southern_europe                ||
    ~~                        |                |                         ~~
    ~~ [south_america]  AAAAAAAAAAAAAAAA    BBBBBBBBB      [asia]        ~~
    || <== brazil-------A north_africa A----B egypt B----middle_east ==> ||
    ||                  A     !A       A    B  !B   B                    ||
    ~~                  AAAAAAAAAAAAAAAA    BBBBBBBBB                    ~~
    ~~                      |    CCCCCCCCCCCCCCC         [asia]          ~~
    ||                      |    C east_africa C-------middle-east ====> || 
    ||                      |    C     !C      C                         ||
    ~~                      |    CCCCCCCCCCCCCCC                         ~~
    ~~                  DDDDDDDDDDDDDDDDDD  |  \                         ~~
    ||                  D central_africa D  |   \                        ||
    ||                  D      !D        D  |    \___                    ||
    ~~                  DDDDDDDDDDDDDDDDDD  |        |                   ~~
    ~~                           EEEEEEEEEEEEEEEE  FFFFFFFFFFFFFF        ~~
    ||                           E south_africa E--F madagascar F        ||
    ||                           E      !E      E  F     !F     F        ||
    ~~                           EEEEEEEEEEEEEEEE  FFFFFFFFFFFFFF        ~~
    ~~                                                                   ~~
    =======================================================================
""",
    'south_america':
r"""
    =======================================================================
    ||                                                                   ||
    ~~                            /\                                     ~~
    ~~                            |                                      ~~
    ||                      [north_america]                              ||
    ||                      central_america                              ||
    ~~                            |                                      ~~
    ~~                      AAAAAAAAAAAAA                                ~~
    ||                      A venezuela A                                ||
    ||                      A     !A    A                                ||
    ~~                      AAAAAAAAAAAAA                                ~~
    ~~                   CCCCCCCCBBBBBBBBBB             [africa]         ~~
    ||                   C peru CB brazil B-----------north_africa ===>  ||
    ||                   C  !C  CB   !B   B                              ||
    ~~                   CCCCCCCCBBBBBBBBBB                              ~~
    ~~                      DDDDDDDDDDDDD                                ~~
    ||                      D argentina D                                ||
    ||                      D    !D     D                                ||
    ~~                      DDDDDDDDDDDDD                                ~~
    ~~                                                                   ~~
    =======================================================================
""",
    'australia':
r"""
    =======================================================================
    ||                                                                   ||
    ~~            /\                                                     ~~
    ~~            |                                                      ~~
    ||           [asia]                                                  ||
    ||        southern_asia                                              ||
    ~~            |                                                      ~~
    ~~      AAAAAAAAAAAAA                      BBBBBBBBBBBBBB            ~~
    ||      A indonesia A----------------------B new_guinea B            ||
    ||      A    !A     A     _________________B     !B     B            ||
    ~~      AAAAAAAAAAAAA    |                 BBBBBBBBBBBBBB            ~~
    ~~            |          |                      |                    ~~
    ||            |          |                      |                    ||
    ||         CCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDDDDDD                ||
    ~~         C western_australia CD eastern_australia D                ~~
    ~~         C       !C          CD       !D          D                ~~
    ||         CCCCCCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDDDDDD                ||
    ||                                                                   ||
    =======================================================================
""",
    # shit just got real
    'asia':
r"""
    =======================================================================
    ||                                                                   ||
    ~~                                                   [north_america] ~~
    ~~                                                     ___ alaska => ~~
    ||                                                     \             ||
    ||            [europe] DDDDDDDDCCCCCCCCCCCBBBBBBBBBBB   |            ||
    ~~          <= russia--D ural DC siberia CB yakutsk B   |            ~~
    ~~                     D  !D  DC    !C  CB   !B     BAAAAAAAAAAAAA   ~~
    ||                     DDDDDDDDC       CBBBBBBBBBBBBBA kamchatka A   ||
    ||            EEEEEEEEEEEEEEEIIIC     CKKKKKKKKKKKKKKA    !A     A   ||
    ~~            E afghanistan EI  IC   CK  irkutsk    KAAAAAAAAAAAAA   ~~
    ~~  [europe]  E     !E      EI   IC CK      !K      K    |           ~~
    || <= russia--E      EEEEEEEEI   IC  CKKKKKKKKKKKKKKK    |           ||
    ||            E      EIIIIIIII   ICCCCJJJJJJJJJJJJ       |           ||
    ~~            E      EI          IIIIIJ mongolia J       |           ~~
    ~~            E      EI   china      IJ    !J    J-----LLLLLLLLL     ~~
    ||            E      EI    !I        IJJJJJJJJJJJJ     L japan L     ||
    ||            E      EI              IIIIIIIIIIIIIII   L   !L  L     ||
    ~~            E      EI                             I  LLLLLLLLL     ~~
    ~~            E      EIIIIIIIIIIIIIIIIIIIIIIIIIIIIII                 ~~
    ||            EEEEEEEEGGGGGGGGGGGGGGGGGGHHHHHHHHHHHHHHHHH            ||
    ||            F       G     india      GH southern_asia H            ||
    ~~  [europe]  F       G       !G       GH      !H       H            ~~
    ~~ <= russia--F       GGGGGGGGGGGGGGGGGGHHHHHHHHHHHHHHHHH            ~~
    ||            F     middle_east    F            |                    ||
    ||             F        !F         F            |                    ||
    ~~              F                  F            |                    ~~
    ~~               FFFFFFFFFF        F            |                    ~~
    ||         [europe]        F       F            |                    ||
    || <==== southern_europe---FFFFFFFFF            |                    ||
    ~~         [africa]        /     |              |                    ~~
    ~~ <======= egypt ________/   [africa]     [australia]               ~~
    ||                           east_africa    indonesia                ||
    ||                               |              |                    ||
    ~~                               \/             \/                   ~~
    ~~                                                                   ~~
    =======================================================================
"""

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
