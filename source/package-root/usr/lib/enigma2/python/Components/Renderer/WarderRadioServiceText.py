from Components.Renderer.Renderer import Renderer
from enigma import eListbox, eListboxServiceContent, gFont
import NavigationInstance


class WarderRadioServiceText(Renderer):
    """TEST124: one-row native service-list painter for Radio sharpness diagnosis."""

    GUI_WIDGET = eListbox

    def __init__(self):
        Renderer.__init__(self)
        self.l = eListboxServiceContent()
        self._filled = False

    def postWidgetCreate(self, instance):
        instance.setContent(self.l)
        self.l.setItemHeight(42)
        self.l.setVisualMode(eListboxServiceContent.visModeSimple)
        self.l.setElementFont(self.l.celServiceName, gFont("Prive4", 33))
        self._refresh()

    def preWidgetRemove(self, instance):
        instance.setContent(None)

    def changed(self, what):
        self._refresh(clear=(what[0] == self.CHANGED_CLEAR))

    def _refresh(self, clear=False):
        if self._filled:
            try:
                self.l.removeCurrent()
            except Exception:
                pass
            self._filled = False
        if clear or self.instance is None:
            return
        try:
            nav = NavigationInstance.instance
            ref = nav and nav.getCurrentlyPlayingServiceReference()
            if ref and ref.valid():
                self.l.addService(ref)
                self.l.FillFinished()
                self._filled = True
        except Exception:
            pass
