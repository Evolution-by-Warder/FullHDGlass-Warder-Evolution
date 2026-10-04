# -*- coding: utf-8 -*-
# Warder Evolution - one composite Radio top-rail widget.

from Components.Renderer.Renderer import Renderer
from Components.config import config
from enigma import eLabel, eTimer
from time import localtime, strftime, time
try:
    from Plugins.Extensions.setupGlass17.weaUtils import toLocale
except Exception:
    def toLocale(value):
        return value


class WarderRadioTop(Renderer):
    GUI_WIDGET = eLabel

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
        # TEST158: one native label; avoid eCanvas.writeText crash on receiver startup.
        date = self._dateText(stamp)
        clock = strftime("%H:%M:%S", localtime(stamp))
        self.instance.setText("%s                         %s                         FullHDGlass17 · Warder Evolution" % (date, clock))

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
