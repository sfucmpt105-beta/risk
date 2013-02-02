from risk.errors.base import RiskGameError

class NoSuchPlayerError(RiskGameError):
    def __init__(self, attempted_player, number_of_players):
        RiskGameError.__init__("attempted to access player: %s but only have" \
            " %s players" % (attempted_player, number_of_players))
