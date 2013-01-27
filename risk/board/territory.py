###############################################################################
## Defines risk territories
#
from sets import Set

import risk.logger

class Territory(object):
    def __init__(self, name, neighbours=[]):
        self.name = name
        self.neighbours = Set(neighbours)
        self.reset(True)

    def reset(self, reset_owner=False):
        self.infantries = 0
        self.artilleries = 0
        self.cavalries = 0
        self.fortification = 0
        if reset_owner:
            self.owner = None

    def add_neighbour(self, neighbour):
        self.neighbours.add(neighbour)
        neighbour.neighbours.add(self)

    def __str__(self):
        return  "[%s]\n" \
                "Owner: %s\n" \
                "Infantries: %s\n" \
                "Cavalries: %s\n" \
                "Artilleries: %s\n" \
                "Fortification: %s" % \
                (self.name, self.owner, self.infantries, self.cavalries, 
                self.artilleries, self.fortification)

    def __repr__(self):
        return self.name

class ContinentBuilder(object):
    def __init__(self, tag):
        self.graph = {}
        self.tag = tag

    def border(self, territory0, territory1):
        self.create_territory_if_needed(territory0)
        self.create_territory_if_needed(territory1)
        self.graph[territory0].add_neighbour(self.graph[territory1])

    def borders(self, list_of_borders):
        for border in list_of_borders:
            self.border(border[0], border[1])
     
    def create_territory_if_needed(self, territory):
        if not self.graph.has_key(territory):
            self.graph[territory] = Territory(territory)

    def validate(self):
        if len(self.graph) == 0:
            risk.logger.warn(
                "graph with tag %s appears to be empty" % self.tag)
        else:
            disjoint = ContinentBuilder.flood_graph(self.graph)
            if len(disjoint) > 0:
                risk.logger.warn(
                    "graph with tag %s has disjoint territories: [%s]" %
                    (self.tag, ', '.join([t.name for t in disjoint]))
                )
                       
    def get_mapping(self):
        self.validate()
        return self.graph

    @staticmethod
    def flood_graph(graph):
        start = graph[graph.keys()[0]]
        visited = Set([start])
        targets = start.neighbours
        while len(targets) > 0:
            current = targets.pop()
            if not current in visited:
                visited.add(current)
                for neighbour in current.neighbours:
                    targets.add(neighbour)
        return Set(graph.values()) - visited
            
    
            
def generate_america_continent():
    builder = ContinentBuilder('generate_america_continent')
    builder.borders([
        ('alaska', 'northwest_territory'), #0
        ('alaska', 'alberta'), #1
        ('northwest_territory', 'greenland'), #2
        ('northwest_territory', 'ontario'), #3
        ('northwest_territory', 'alberta'), #4
        ('alberta', 'ontario'), #5
        ('alberta', 'western_united_states'), #6
        ('greenland', 'eastern_canada'), #7
        ('greenland', 'ontario'), #8
        ('ontario', 'eastern_canada'), #9
        ('ontario', 'eastern_united_states'), #10
        ('ontario', 'western_united_states'), #11
        ('western_united_states', 'eastern_united_states'), #12
        ('western_united_states', 'central_america'), #13
        ('eastern_canada', 'eastern_united_states'), #14
        ('eastern_united_states', 'central_america'), #15
    ])
    return builder.get_mapping()

