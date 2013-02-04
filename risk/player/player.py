from risk import commands
from risk.printer import risk_input

class AbstractRiskPlayer(object):
    def __init__(self, name):
        self.name = name
        self.is_bot = False

    def take_turn(self, game_master):
        raise NotImplementedError

# Qwerrrrrrk
class HumonRiskPlayer(AbstractRiskPlayer):
    def __init__(self, name):
        # Python sucks at this, base refers to base class
        AbstractRiskPlayer.__init__(self, name)

    def take_turn(self, game_master):
        commands.prompt_user(self, game_master)

    def pick_territory(self, choices):
        risk_input("Choose a territory...")
        print choices
