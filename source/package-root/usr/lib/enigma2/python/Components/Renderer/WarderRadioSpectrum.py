# -*- coding: utf-8 -*-
# Warder Evolution - lightweight decorative Radio spectrum.
# Visual effect only: deliberately does not claim to analyse programme audio.

from Components.Renderer.Renderer import Renderer
from enigma import eCanvas, eRect, eTimer, gRGB


class WarderRadioSpectrum(Renderer):
    GUI_WIDGET = eCanvas

    def __init__(self):
        Renderer.__init__(self)
        self._running = False
        self._frame = 0
        self._bars = 18
        self._levels = [2] * self._bars
        self._peaks = [2] * self._bars
        self._holds = [0] * self._bars
        self._timer = eTimer()
        try:
            self._timer_conn = self._timer.timeout.connect(self._tick)
        except AttributeError:
            self._timer.callback.append(self._tick)

    def _target(self, index):
        # Small deterministic multi-wave motion: no random generator, I/O, FFT or subprocess.
        a = (self._frame * (3 + (index % 4)) + index * 11) % 34
        b = (self._frame * (2 + (index % 3)) + index * 7) % 26
        a = 33 - abs(33 - (a * 2))
        b = 25 - abs(25 - (b * 2))
        return max(3, min(30, 4 + ((a * 2 + b) // 3)))

    def _color(self, step):
        if step >= 27:
            return gRGB(255, 48, 24, 0)
        if step >= 22:
            return gRGB(255, 145, 20, 0)
        if step >= 17:
            return gRGB(255, 220, 35, 0)
        if step >= 10:
            return gRGB(30, 205, 255, 0)
        return gRGB(20, 115, 255, 0)

    def _paint(self):
        if self.instance is None:
            return
        self.instance.clear(gRGB(0, 0, 0, 255))
        width, height = 350, 126
        gap = 4
        barw = 15
        unit = 3
        content_width = self._bars * barw + (self._bars - 1) * gap
        left = max(0, (width - content_width) // 2)
        base = height - 5
        for i in range(self._bars):
            level = self._levels[i]
            x = left + i * (barw + gap)
            for step in range(level):
                y = base - ((step + 1) * unit)
                self.instance.fillRect(eRect(x, y, barw, max(1, unit - 1)), self._color(step))
            peak = self._peaks[i]
            py = base - ((peak + 1) * unit)
            self.instance.fillRect(eRect(x, py, barw, 2), self._color(peak))

    def _tick(self):
        if not self._running:
            return
        self._frame = (self._frame + 1) % 4096
        for i in range(self._bars):
            target = self._target(i)
            current = self._levels[i]
            if target > current:
                current = min(target, current + 4)
            else:
                current = max(target, current - 2)
            self._levels[i] = current
            if current >= self._peaks[i]:
                self._peaks[i] = current
                self._holds[i] = 2
            elif self._holds[i] > 0:
                self._holds[i] -= 1
            else:
                self._peaks[i] = max(current, self._peaks[i] - 1)
        self._paint()

    def postWidgetCreate(self, instance):
        # Native RdsInfoDisplay does not reliably forward Screen onShow to
        # custom renderers on all Enigma2 images. Start from widget creation.
        self._running = True
        self._paint()
        self._timer.start(200)

    def preWidgetRemove(self, instance):
        self._running = False
        self._timer.stop()

    def changed(self, what):
        if self.instance is not None and not self._running:
            self._running = True
            self._timer.start(200)
        if self._running:
            self._paint()

    def onShow(self):
        self._running = True
        self._paint()
        self._timer.start(200)

    def onHide(self):
        self._running = False
        self._timer.stop()
