"""Keep LiveTV exclusive to the main configuration menu, including resume."""
from Components.Renderer.Pig import Pig


class WarderSettingsPig(Pig):
    def applySkin(self, desktop, parent):
        self.warder_screen = parent
        return Pig.applySkin(self, desktop, parent)

    def onShow(self):
        if getattr(getattr(self, 'warder_screen', None), 'isMainMenu', True):
            Pig.onShow(self)
            if self.instance is not None:
                self.instance.show()
        else:
            Pig.onHide(self)
            if self.instance is not None:
                self.instance.hide()
