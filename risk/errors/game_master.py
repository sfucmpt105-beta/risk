from risk.errors.base import RiskGameError

class GameMasterError(RiskGameError):
    def __init__(self, msg):
        RiskGameError.__init__(self, msg)

class NoSuchPlayerError(GameMasterError):
    def __init__(self, attempted_player, number_of_players):
        GameMasterError.__init__(self, "attempted to access player: %s but only have" \
            " %s players" % (attempted_player, number_of_players))

class NotEnoughReserves(GameMasterError):
    def __init__(self, player):
        GameMasterError.__init__(self,
            "%s has no more reserve troops to deploy" % player.name)

class TerritoryNotOwnedByPlayer(GameMasterError):
    def __init__(self, territory, player):
        GameMasterError.__init__(self,
            "%s does not own territory %s" % (player.name, territory.name))

class DeployRangeError(GameMasterError):
    def __init__(self, number_of_armies):
        GameMasterError.__init__(self,
            "%s is not a valid number of armies to deploy" % number_of_armies)

class MoveRangeError(GameMasterError):
    def __init__(self, number_of_armies):
        GameMasterError.__init__(self, "You do not have %s armies to move" % number_of_armies)

class NotNeighbours(GameMasterError):
    def __init__(self, origin, destination):
        GameMasterError.__init__(self, "You can't move troops from %s and %s" % (origin, destination))
