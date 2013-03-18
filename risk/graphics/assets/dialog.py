import risk
import risk.graphics.assets

from risk.graphics.assets.base import PicassoAsset
from risk.graphics.assets.text import TextAsset

class DialogAsset(PicassoAsset):
    def __init__(self, x, y, msg, validator=None):
        self.text_asset = TextAsset(0, 0, msg)
        self.validator = validator
        PicassoAsset.__init__(self, None, x, y)

    def draw(self):
        return self.text_asset.draw()

    def set_text(self, msg):
        self.text_asset.render_text(msg)
