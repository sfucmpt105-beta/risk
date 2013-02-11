from risk.errors.base import RiskGameError

class GameMasterError(RiskGameError):
    def __init__(self, msg):
        RiskGameError.__init__(msg)

class NoSuchPlayerError(GameMasterError):
    def __init__(self, attempted_player, number_of_players):
        GameMasterError.__init__("attempted to access player: %s but only have" \
            " %s players" % (attempted_player, number_of_players))

class NotEnoughReserves(GameMasterError):
    def __init__(self, player):
        GameMasterError.__init__(
            "%s has no more reserve troops to deploy" % player.name)

class TerritoryNotOwnedByPlayer(GameMasterError):
    def __init__(self, territory, player):
        GameMasterError.__init__(
            "%s does not own territory %s" % (player.name, territory.name))
