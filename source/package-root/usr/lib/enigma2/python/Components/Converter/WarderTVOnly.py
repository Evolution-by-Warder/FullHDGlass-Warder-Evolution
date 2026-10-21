# -*- coding: utf-8 -*-
# Keep this independent of WarderRadioOnly: the skin loader caches by isinstance.
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Converter.WarderRadioOnly import is_radio_source


class WarderTVOnly(Converter):
    def __init__(self, type):
        Converter.__init__(self, type)

    @cached
    def getBoolean(self):
        return not is_radio_source(self.source)

    boolean = property(getBoolean)

    def changed(self, what):
        Converter.changed(self, what)
