import risk
from risk.errors.base import RiskGameError

class UserQuitInput(KeyboardInterrupt):
    def __init__(self):
        KeyboardInterrupt.__init__(self, 'user wants to quit')
