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
        # Read the active DVB service directly first. The marker is written by
        # the plugin at service-start and can otherwise lag the skin converter.
        try:
            nav = NavigationInstance.instance
            ref = nav and nav.getCurrentlyPlayingServiceReference()
            fields = ref.toString().split(":") if ref is not None else []
            if len(fields) > 2:
                return fields[2].upper() in ("2", "A")
        except Exception:
            pass
        try:
            with open("/tmp/warder-radio-current", "r") as marker:
                return marker.read(8).strip() == "A"
        except Exception:
            return False

    boolean = property(getBoolean)

    def changed(self, what):
        Converter.changed(self, what)
