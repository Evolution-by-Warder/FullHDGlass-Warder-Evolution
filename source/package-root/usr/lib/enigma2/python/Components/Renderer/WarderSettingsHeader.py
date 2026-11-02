"""Clip the existing full-size Warder artwork to the banner; no per-tick decoding."""
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eSize, eWidget, getDesktop


class WarderSettingsHeader(Renderer):
    GUI_WIDGET = eWidget

    def __init__(self):
        Renderer.__init__(self)
        self.picture = None

    def postWidgetCreate(self, instance):
        self.picture = ePixmap(instance)
        size = getDesktop(0).size()
        self.picture.resize(eSize(size.width(), size.height()))
        self.picture.setScale(1)
        self.picture.setPixmapFromFile('/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/images/warder-settings-background.png')
        self.picture.show()

    def changed(self, what):
        pass

    def preWidgetRemove(self, instance):
        self.picture = None
