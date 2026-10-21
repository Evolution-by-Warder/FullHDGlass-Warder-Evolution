# -*- coding: utf-8 -*-
# Warder Evolution - true only while the current service is Radio.

from Components.Converter.Converter import Converter
from Components.Element import cached
import NavigationInstance


class WarderRadioOnly(Converter):
    def __init__(self, type):
        Converter.__init__(self, type)

    @cached
    def getBoolean(self):
        # The service-start hook writes this marker before the skin redraws.
        # Prefer it over NavigationInstance, which can briefly still report
        # the previous TV service during a TV -> radio transition.
        try:
            with open("/tmp/warder-radio-current", "r") as marker:
                state = marker.read(8).strip().upper()
            if state == "A":
                return True
            if state == "TV":
                return False
        except Exception:
            pass
        try:
            nav = NavigationInstance.instance
            ref = nav and nav.getCurrentlyPlayingServiceReference()
            fields = ref.toString().split(":") if ref is not None else []
            if len(fields) > 2:
                return fields[2].upper() in ("2", "A")
        except Exception:
            pass
        return False

    boolean = property(getBoolean)

    def changed(self, what):
        Converter.changed(self, what)
