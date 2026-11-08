"""Visibility of the optional EPG/Prime Time separator.

The separator is a normal 1px skin label, with visibility controlled by the
current setting rather than by ChannelSelection's creation-time XML.
"""
from Components.Renderer.Renderer import Renderer
from Components.config import config
from enigma import eLabel


class WarderPrimeTimeDivider(Renderer):
    GUI_WIDGET = eLabel

    def changed(self, what):
        if not self.instance:
            return
        try:
            enabled = bool(config.plugins.warderEvolutionPrimeTime.enabled.value)
        except (AttributeError, TypeError, ValueError):
            enabled = False
        if enabled and what[0] != self.CHANGED_CLEAR:
            self.instance.show()
        else:
            self.instance.hide()
