# -*- coding: utf-8 -*-
# Warder Evolution - one composite Radio top-rail widget.

from Components.Renderer.Renderer import Renderer
from Components.config import config
from enigma import eCanvas, eRect, eSize, eTimer, gFont, gRGB, RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_HALIGN_RIGHT, RT_VALIGN_CENTER
from time import localtime, strftime, time
try:
    from Plugins.Extensions.setupGlass17.weaUtils import toLocale
except Exception:
    def toLocale(value):
        return value


class WarderRadioTop(Renderer):
    GUI_WIDGET = eCanvas

    def __init__(self):
        Renderer.__init__(self)
        self._timer = eTimer()
        try:
            self._timer_conn = self._timer.timeout.connect(self._paint)
        except AttributeError:
            self._timer.callback.append(self._paint)

    def _dateText(self, stamp):
        fmt = "%A  %d.%B %Y"
        try:
            if config.plugins.setupGlass17.par134.value != "D":
                fmt = config.plugins.setupGlass17.par134.value
            if config.plugins.setupGlass17.par138.value:
                fmt = fmt.replace("%H", "%-H")
            if config.plugins.setupGlass17.par188.value:
                fmt = fmt.replace("%d", "%-d").replace("%m", "%-m")
        except Exception:
            pass
        try:
            return toLocale(strftime(fmt, localtime(stamp)))
        except Exception:
            return strftime(fmt, localtime(stamp))

    def _paint(self):
        if self.instance is None:
            return
        try:
            stamp = self.source.time
        except Exception:
            stamp = None
        if stamp is None:
            stamp = time()
        self.instance.clear(gRGB(0, 0, 0, 255))
        # One canvas, three segments. All share the exact same y/h and vertical centre.
        h = 58
        self.instance.writeText(eRect(0, 0, 610, h), gRGB(229, 178, 67, 0), gRGB(0, 0, 0, 255), gFont("Prive4", 30), self._dateText(stamp), RT_HALIGN_LEFT | RT_VALIGN_CENTER)
        self.instance.writeText(eRect(683, 0, 340, h), gRGB(238, 238, 238, 0), gRGB(0, 0, 0, 255), gFont("Prive4", 38), strftime("%H:%M:%S", localtime(stamp)), RT_HALIGN_CENTER | RT_VALIGN_CENTER)
        self.instance.writeText(eRect(1158, 0, 580, h), gRGB(176, 176, 176, 0), gRGB(0, 0, 0, 255), gFont("Prive4", 25), "FullHDGlass17 · Warder Evolution", RT_HALIGN_RIGHT | RT_VALIGN_CENTER)

    def postWidgetCreate(self, instance):
        self._paint()
        self._timer.start(500)

    def preWidgetRemove(self, instance):
        self._timer.stop()

    def changed(self, what):
        self._paint()

    def onShow(self):
        self._paint()
        self._timer.start(500)

    def onHide(self):
        self._timer.stop()
