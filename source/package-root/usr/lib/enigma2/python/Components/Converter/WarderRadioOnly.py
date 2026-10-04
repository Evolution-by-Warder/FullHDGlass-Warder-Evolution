# -*- coding: utf-8 -*-
# Warder Evolution - true only while the current service is Radio.

from Components.Converter.Converter import Converter
from Components.Element import cached


class WarderRadioOnly(Converter):
    def __init__(self, type):
        Converter.__init__(self, type)

    @cached
    def getBoolean(self):
        try:
            with open("/tmp/warder-radio-current", "r") as marker:
                return marker.read(8).strip() == "A"
        except Exception:
            return False

    boolean = property(getBoolean)

    def changed(self, what):
        Converter.changed(self, what)
