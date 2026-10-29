# -*- coding: utf-8 -*-
"""Decorative radio spectrum: one native pixmap update per frame.

The approved 84 x 3px artwork is rendered by the build tool, never by the
receiver GUI thread. Do not reintroduce thousands of eCanvas.fillRect calls.
"""
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, eTimer
from Tools.LoadPixmap import LoadPixmap


_FRAME_ROOT = "/usr/share/enigma2/hd_glass17/warder-spectrum/"
_FRAME_COUNT = 48
# Shared across RadioInfoBar / RdsDisplay / RdsInfoDisplay. At most 8.1 MiB
# of decoded RGBA pixels, not a separate allocation for every renderer.
_FRAMES = [None] * _FRAME_COUNT


class WarderRadioSpectrum(Renderer):
    GUI_WIDGET = ePixmap

    def __init__(self):
        Renderer.__init__(self)
        self._running = False
        self._hidden = False
        self._failed = False
        self._frame = 0
        self._direction = 1
        self._interval = 100
        self._timer = eTimer()
        try:
            self._timer_conn = self._timer.timeout.connect(self._tick)
        except AttributeError:
            self._timer.callback.append(self._tick)

    def _start(self):
        if self.instance is not None and not self._hidden and not self._failed and not self._running:
            self._running = True
            self._timer.start(self._interval, True)

    def _tick(self):
        if not self._running or self._hidden or self.instance is None:
            return
        # Parent visibility matters too: some native RDS screens omit renderer
        # onHide notifications. Do no decoding or painting behind a hidden parent.
        if not self.instance.isVisible():
            self._timer.start(500, True)
            return
        try:
            frame = _FRAMES[self._frame]
            if frame is None:
                # Decode at most ONE small PNG per callback, once per shared
                # frame. Disable the separate global Enigma pixmap cache.
                frame = LoadPixmap(_FRAME_ROOT + "frame-%02d.png" % self._frame, cached=False)
                if frame is None:
                    raise ValueError("Unavailable spectrum frame")
                _FRAMES[self._frame] = frame
            self.instance.setPixmap(frame)
        except Exception:
            # A missing/corrupt optional visual must never stall radio or create
            # a retry/log storm. Keep the last good frame until GUI restart.
            self._failed = True
            self._running = False
            self._timer.stop()
            return
        self._frame += self._direction
        if self._frame >= _FRAME_COUNT:
            self._direction = -1
            self._frame = _FRAME_COUNT - 2
        elif self._frame < 0:
            self._direction = 1
            self._frame = 1
        # One-shot, rearmed AFTER the update: a slow box cannot accumulate
        # repeating timer work faster than its GUI can consume it.
        self._timer.start(self._interval, True)

    def postWidgetCreate(self, instance):
        Renderer.postWidgetCreate(self, instance)
        self.instance.setAlphatest(1)
        self._hidden = False
        # Polling visibility also supports native RDS paths without onShow.
        self._start()

    def preWidgetRemove(self, instance):
        self.onHide()
        Renderer.preWidgetRemove(self, instance)

    def changed(self, what):
        # Service metadata can change often. It must not trigger extra paints
        # or restart a timer that was explicitly stopped by onHide.
        self._start()

    def onShow(self):
        self._hidden = False
        self._start()

    def onHide(self):
        self._hidden = True
        self._running = False
        self._timer.stop()
