"""Optional Prime Time label driven by the selected ServiceEvent source.

Keep the renderer independent from ChannelSelection screen classes and do not
change image-owned code. Layout positions are assigned by individual skin
templates only after their free space has been verified.
"""
from time import time

from Components.Renderer.Renderer import Renderer
from Components.VariableText import VariableText
from Components.config import config
from enigma import eLabel, eEPGCache
from Plugins.Extensions.setupGlass17.warderPrimeTime import prime_time_event


class WarderPrimeTime(VariableText, Renderer):
    GUI_WIDGET = eLabel

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self._cache = eEPGCache.getInstance()

    def changed(self, what):
        if not self.instance:
            return
        try:
            enabled = config.plugins.setupGlass17.warderPrimeTimeEnabled.value
            clock = config.plugins.setupGlass17.warderPrimeTimeClock.value
            hour, minute = int(clock[0]), int(clock[1])
        except (AttributeError, ValueError, TypeError, IndexError):
            enabled, hour, minute = False, 20, 25
        if not enabled or what[0] == self.CHANGED_CLEAR:
            self.text = ""
            self.instance.hide()
            return
        try:
            service = self.source.service
            if service is None:
                self.text = ""
                self.instance.hide()
                return
            # Exclude bouquet folders and markers.
            if getattr(service, "flags", 0) & 0x40:
                self.text = ""
                self.instance.hide()
                return
            result = prime_time_event(self._cache, service, time(), hour, minute)
        except (AttributeError, RuntimeError, TypeError, ValueError):
            result = None
        self.text = "Prime Time %02d:%02d: %s" % (hour, minute, result[1]) if result else (
            "Prime Time %02d:%02d: EPG unavailable" % (hour, minute))
        self.instance.show()
