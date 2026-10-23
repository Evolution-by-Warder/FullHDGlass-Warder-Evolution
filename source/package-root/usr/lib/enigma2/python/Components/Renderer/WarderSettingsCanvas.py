"""Show the settings colour sample only while a colour is being edited.

Uses the native Canvas draw pipeline; normal values and the main menu have no
visible canvas. Source visibility is set before its existing flush() call.
"""
from Components.Renderer.Canvas import Canvas


class WarderSettingsCanvas(Canvas):
    def __init__(self):
        Canvas.__init__(self)
        self.hide()

    def pullUpdates(self):
        Canvas.pullUpdates(self)
        self.visible = bool(getattr(self.source, "warder_sample_visible", False))
