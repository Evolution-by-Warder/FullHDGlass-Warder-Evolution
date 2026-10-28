"""Compatibility slot: the native RDS window now owns the sole radio header.

Earlier InfoPanel mirrors could overprint a second text layer. Keep the renderer
name for saved templates, but never draw duplicate date/clock/brand glyphs.
"""
from Components.Renderer.Renderer import Renderer
from enigma import eLabel


class WarderRadioInfoTop(Renderer):
    GUI_WIDGET = eLabel

    def postWidgetCreate(self, instance):
        instance.setText('')

    def changed(self, what):
        if self.instance is not None:self.instance.setText('')
