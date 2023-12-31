import risk

from risk.graphics.assets.text import TextAsset

class ReserveCountAsset(TextAsset):
    def __init__(self, player):
        self.player = player
        TextAsset.__init__(self, 100, 600, '')

    def draw(self):
        self.render_text("%s reserves left" % self.player.reserves)
        return TextAsset.draw(self)

