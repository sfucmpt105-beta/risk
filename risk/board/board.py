###############################################################################
## defines the board object as well as some board generation utilities
#
import territory

class RiskBoard(object):
    def __init__(self, continents):
        self.continents = continents

def get_standard_risk_map():
    return {
        'north_america': territory.generate_america_continent(),
        'south_america': {},
        'europe': {},
        'africa': {},
        'asia': {},
        'austrailia': {},
    }
    
def generate_empty_board():
    return RiskBoard(get_standard_risk_map())
