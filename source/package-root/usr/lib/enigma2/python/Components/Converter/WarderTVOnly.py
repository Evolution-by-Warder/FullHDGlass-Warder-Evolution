# -*- coding: utf-8 -*-
# Warder Evolution - true only while the current service is television.

from Components.Element import cached
from Components.Converter.WarderRadioOnly import WarderRadioOnly


class WarderTVOnly(WarderRadioOnly):
    @cached
    def getBoolean(self):
        return not WarderRadioOnly.getBoolean(self)

    boolean = property(getBoolean)
