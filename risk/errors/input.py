import risk
from risk.errors.base import RiskGameError

class UserQuitInput(RiskGameError):
    def __init__(self):
        RiskGameError.__init__(self, 'user wants to quit')
