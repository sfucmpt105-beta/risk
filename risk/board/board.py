###############################################################################
## defines the board object as well as some board generation utilities
#
import territory

import risk.logger
from risk.errors.board import *

class RiskBoard(object):
    def __init__(self, continents):
        self.continents = continents

    def territories(self):
        return dict([territory for continent in self.continents.values() 
                for territory in continent.items()])

    def __getitem__(self, territory_name):
        try:
            return self.territories()[territory_name]
        except KeyError:
            raise NoSuchTerritory(territory_name)

def get_standard_risk_map():
    risk.logger.debug('Generating standard map...')
    board = {
        'north_america': territory.generate_north_america_continent(),
        'south_america': territory.generate_south_america_continent(),
        'europe': territory.generate_europe_continent(),
        'africa': territory.generate_africa_continent(),
        'asia': territory.generate_asia_continent(),
        'australia': territory.generate_australia_continent(),
    }
    risk.logger.debug('Continent generated, creating inter-continental paths')
    board['north_america']['greenland'].add_neighbour(
        board['europe']['iceland'])
    board['south_america']['brazil'].add_neighbour(
        board['africa']['north_africa'])
    board['africa']['egypt'].add_neighbour(
        board['europe']['southern_europe'])
    board['asia']['southern_asia'].add_neighbour(
        board['australia']['indonesia'])
    board['africa']['east_africa'].add_neighbour(
        board['asia']['middle_east'])
    risk.logger.debug('Map generated!')
    return board
    
def generate_empty_board():
    return RiskBoard(get_standard_risk_map())

def generate_mini_board():
    return RiskBoard({'mini': territory.generate_australia_continent()})
