from risk.errors.base import RiskGameError

class BoardError(RiskGameError):
    def __init__(self, msg):
        RiskGameError.__init__(self, msg)

class NoSuchTerritory(BoardError):
    def __init__(self, territory):
        BoardError.__init__(self, "no such territory in board: %s" % territory)
