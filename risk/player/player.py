from risk import commands
from risk.printer import risk_input

class AbstractRiskPlayer(object):
    def __init__(self, name):
        self.name = name
        self.is_bot = False

    def take_turn(self, game_master):
        raise NotImplementedError

    def choose_territory(self, available):
        raise NotImplementedError

# Qwerrrrrrk
class HumonRiskPlayer(AbstractRiskPlayer):
    def __init__(self, name):
        # Python sucks at this, base refers to base class
        AbstractRiskPlayer.__init__(self, name)

    def take_turn(self, game_master):
        commands.prompt_user(self, game_master)

    def choose_territory(self, availables):
        print "%s's turn..." % self.name
        return commands.prompt_choose_territory(availables)
