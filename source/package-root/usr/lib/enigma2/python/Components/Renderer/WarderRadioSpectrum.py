# -*- coding: utf-8 -*-
# Warder Evolution - lightweight decorative Radio spectrum.
# Visual effect only: deliberately does not claim to analyse programme audio.

from math import ceil, exp, pi, sin

from Components.Renderer.Renderer import Renderer
from enigma import eCanvas, eRect, eTimer, gRGB, eSize
from skin import parseColor


class WarderRadioSpectrum(Renderer):
    GUI_WIDGET = eCanvas

    def __init__(self):
        Renderer.__init__(self)
        self._running = False
        self._hidden = False
        self._frame = 0
        # Owner-approved 350x126 preview: 84 fine stacks, 3px bars / 1px gaps.
        self._bars = 84
        self._interval = 50
        self._elapsed = 0.0
        self._color_time = 0.0
        self._levels = [2] * self._bars
        self._peaks = [2] * self._bars
        self._holds = [0] * self._bars
        self._visible = [2.0] * self._bars
        self._visible_peaks = [2.0] * self._bars
        # Native colour objects are reused; no allocation per drawn segment.
        self._palette = []
        for hue in range(360):
            # HSL( hue, 88%, 55.5% ), without adding a receiver dependency.
            chroma = (1.0 - abs(2.0 * 0.555 - 1.0)) * 0.88
            secondary = chroma * (1.0 - abs((hue / 60.0) % 2.0 - 1.0))
            offset = 0.555 - chroma / 2.0
            red, green, blue = ((chroma, secondary, 0), (secondary, chroma, 0),
                                (0, chroma, secondary), (0, secondary, chroma),
                                (secondary, 0, chroma), (chroma, 0, secondary))[hue // 60]
            self._palette.append(gRGB(int((red + offset) * 255), int((green + offset) * 255), int((blue + offset) * 255), 0))
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

    def _color(self, step, index=0, level=30.0, flow=0.0):
        # Blue/cyan/green/yellow/orange/red across each visible stack, with a
        # slow travelling colour drift. Flat pixels: no neon or glow layers.
        fraction = max(0.0, min(1.0, step / max(1.0, level - 1.0)))
        detail = 5.0 * sin(self._color_time * 0.37 + fraction * pi + index * 0.04)
        hue = int(238.0 * (1.0 - fraction) + flow + detail) % 360
        return self._palette[hue]

    def _paint(self):
        if self.instance is None:
            return
        self.instance.clear(gRGB(0, 0, 0, 255))
        width, height = 350, 126
        gap = 1
        barw = 3
        unit = 3
        content_width = self._bars * barw + (self._bars - 1) * gap
        left = max(0, (width - content_width) // 2)
        base = height - 5
        for i in range(self._bars):
            level = self._visible[i]
            x = left + i * (barw + gap)
            flow = 13.0 * sin(self._color_time * 0.65 - i * 0.105)
            for step in range(int(ceil(level))):
                y = base - ((step + 1) * unit)
                coverage = min(1.0, level - step)
                segment_height = int((unit - 1) * coverage + 0.5)
                if segment_height:
                    self.instance.fillRect(eRect(x, y + unit - 1 - segment_height, barw, segment_height), self._color(step, i, level, flow))
            peak = self._visible_peaks[i]
            py = int(round(base - ((peak + 1.0) * unit)))
            self.instance.fillRect(eRect(x, py, barw, 2), self._color(peak, i, peak + 1.0, flow))

    def _advanceLevels(self):
        # Preserve the independent 110ms target/peak scheduler. Rendering is
        # interpolated at 20fps instead of making every target jump a frame.
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

    def _tick(self):
        if not self._running:
            return
        self._frame = (self._frame + 1) % 4096
        dt = self._interval / 1000.0
        self._elapsed += dt
        self._color_time += dt
        while self._elapsed >= 0.11:
            self._advanceLevels()
            self._elapsed -= 0.11
        for i in range(self._bars):
            rate = 22.0 if self._levels[i] > self._visible[i] else 15.0
            self._visible[i] += (self._levels[i] - self._visible[i]) * (1.0 - exp(-rate * dt))
            self._visible_peaks[i] += (self._peaks[i] - self._visible_peaks[i]) * (1.0 - exp(-18.0 * dt))
        self._paint()

    def postWidgetCreate(self, instance):
        # Let the base Renderer complete widget/source binding first. This is
        # required by some OpenATV/eCanvas builds before drawing is accepted.
        Renderer.postWidgetCreate(self, instance)
        self._hidden = False
        # Native RdsInfoDisplay does not reliably forward Screen onShow to
        # custom renderers on all Enigma2 images. Start from widget creation.
        self._running = True
        self._paint()
        self._timer.start(self._interval)

    def preWidgetRemove(self, instance):
        self._hidden = True
        self._running = False
        self._timer.stop()
        Renderer.preWidgetRemove(self, instance)

    def changed(self, what):
        if self._hidden:
            return
        if self.instance is not None and not self._running:
            self._running = True
            self._timer.start(self._interval)
        if self._running:
            self._paint()

    def onShow(self):
        self._hidden = False
        self._running = True
        self._paint()
        self._timer.start(self._interval)

    def onHide(self):
        self._hidden = True
        self._running = False
        self._timer.stop()
