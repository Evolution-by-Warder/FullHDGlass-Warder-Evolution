"""Hide an existing EPG label while optional Prime Time occupies its own cell.

Append after the label's original converter, so the disabled-by-default skin
keeps its original value and format. No animation or screen-class monkeypatch.
"""
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config


class WarderPrimeTimeGate(Converter):
    def __init__(self, type):
        Converter.__init__(self, type)

    @cached
    def getText(self):
        try:
            if config.plugins.warderEvolutionPrimeTime.enabled.value:
                return ""
        except AttributeError:
            pass
        return self.source.text or ""

    text = property(getText)
