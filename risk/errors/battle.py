from risk.errors.base import RiskGameError

class RiskBattleError(RiskGameError):
    pass

class NonNeighbours(RiskBattleError):
    def __init__(self, origin, target):
        RiskGameError.__init__(self, "%s and %s aren't neighbours!" % \
            (origin.name, target.name))

class AttackingThyself(RiskBattleError):
    def __init__(self, origin, target):
        RiskGameError.__init__(self, "You own both %s and %s!" % \
            (origin.name, target.name))

class InsufficientAttackingArmies(RiskBattleError):
    def __init__(self, origin):
        RiskGameError.__init__(self, "%s doesn't have enough armies to " \
            "attack, minimum is 2" % (origin.name))

