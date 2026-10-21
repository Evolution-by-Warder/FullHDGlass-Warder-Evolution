# -*- coding: utf-8 -*-
# Warder Evolution - lightweight decorative Radio spectrum.
# Visual effect only: deliberately does not claim to analyse programme audio.

from Components.Renderer.Renderer import Renderer
from enigma import eCanvas, eRect, eTimer, gRGB, eSize
from skin import parseColor


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
        # Per-bar deterministic state.  Keep the effect self-contained and
        # receiver-safe, but avoid driving every bar from one shared wave.
        self._seeds = [((i + 1) * 1103515245 + 12345) & 0x7fffffff for i in range(self._bars)]
        self._targets = [3 + (self._seeds[i] % 28) for i in range(self._bars)]
        self._wait = [i % 4 for i in range(self._bars)]
        self._timer = eTimer()
        try:
            self._timer_conn = self._timer.timeout.connect(self._tick)
        except AttributeError:
            self._timer.callback.append(self._tick)

    def applySkin(self, desktop, parent):
        # Mirror the receiver-proven FullHDGlass17 g17VolumeGauge eCanvas path:
        # explicitly size the native canvas before Renderer.applySkin().
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == "size":
                x, y = value.split(",")
                self.instance.setSize(eSize(int(x), int(y)))
                attribs.append((attrib, value))
            elif attrib == "backgroundColor":
                self.instance.clear(parseColor(value))
            else:
                attribs.append((attrib, value))
        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    def _nextTarget(self, index):
        # Independent deterministic pseudo-random stream per bar.  No random
        # module, audio probing, I/O or subprocesses; only visual decoration.
        seed = (self._seeds[index] * 1103515245 + 12345 + (index * 97)) & 0x7fffffff
        self._seeds[index] = seed
        # Bias most motion into the useful middle range, with occasional peaks.
        a = (seed >> 8) % 28
        b = (seed >> 17) % 28
        return max(3, min(30, 3 + ((a + b) // 2)))

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
            if self._wait[i] > 0:
                self._wait[i] -= 1
            elif self._levels[i] == self._targets[i]:
                self._targets[i] = self._nextTarget(i)
                self._wait[i] = (self._seeds[i] >> 5) % 4
            target = self._targets[i]
            current = self._levels[i]
            if target > current:
                # Different rise rates prevent a marching/synchronous look.
                current = min(target, current + 2 + ((self._seeds[i] >> 3) % 3))
            else:
                current = max(target, current - 1 - ((self._seeds[i] >> 6) % 2))
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
        # Let the base Renderer complete widget/source binding first. This is
        # required by some OpenATV/eCanvas builds before drawing is accepted.
        Renderer.postWidgetCreate(self, instance)
        # Native RdsInfoDisplay does not reliably forward Screen onShow to
        # custom renderers on all Enigma2 images. Start from widget creation.
        self._running = True
        self._paint()
        self._timer.start(140)

    def preWidgetRemove(self, instance):
        self._running = False
        self._timer.stop()
        Renderer.preWidgetRemove(self, instance)

    def changed(self, what):
        if self.instance is not None and not self._running:
            self._running = True
            self._timer.start(140)
        if self._running:
            self._paint()

    def onShow(self):
        self._running = True
        self._paint()
        self._timer.start(140)

    def onHide(self):
        self._running = False
        self._timer.stop()
