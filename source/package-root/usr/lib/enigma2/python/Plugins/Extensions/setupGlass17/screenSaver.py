# -*- coding: utf-8 -*-
"""FullHDGlass radio-only OLED saver, matching the Warder Radio plugin layout.

This screen is presented modally by warderRadioSaverController only after a
configurable idle period. Native labels/pixmaps are used; internet cover
lookup stays in a bounded background worker and never blocks Enigma2 GUI.
"""
import os
import threading
import time

from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.config import config
from Components.Converter.WarderRadioOnly import is_native_dab
from Components.Converter.WarderRadioMetadata import current_song, native_song, stream_url
from enigma import eTimer, iServiceInformation
from Tools.LoadPixmap import LoadPixmap

from .warderResolution import Screen, ePoint
from .warderRadioSaverLayout import make_widgets, bounded_motion
from .warderUserPicons import selected_source, find_png

_MARKUP, _POSITIONS = make_widgets()


def _service_name(ref, service):
    try:
        info = service and service.info()
        if info:
            name = info.getName() or ""
            if name:
                return name.strip()
    except Exception:
        pass
    try:
        from ServiceReference import ServiceReference
        return (ServiceReference(ref).getServiceName() or "").strip()
    except Exception:
        return ""


def _service_group(ref, service):
    if is_native_dab(ref):
        kind = "DAB / DAB+"
    elif stream_url(ref):
        kind = "INTERNET RADIO"
    else:
        kind = "DVB RADIO"
    try:
        info = service and service.info()
        name = info.getInfoString(iServiceInformation.sProvider) if info else ""
        if name and str(name).strip():
            return str(name).strip(), kind
    except Exception:
        pass
    return kind, kind


def _picon_path(ref):
    try:
        ref_text = ref.toString()
        stem = "_".join(ref_text.split(":")[:10]).upper().rstrip("_")
        enabled, directory = selected_source(config)
        if enabled:
            return find_png(directory, stem)
        from Components.Renderer.Picon import getPiconName
        name = getPiconName(ref_text)
        if name and os.path.isfile(name):
            return name
    except Exception:
        pass
    try:
        root = config.plugins.setupGlass17.par39.value
        for folder in (os.path.join(root, "picon", "radio"),
                       os.path.join(root, "picon")):
            result = find_png(folder, stem)
            if result:
                return result
    except Exception:
        pass
    return ""


class ScreenSaverScreen(Screen):
    skin = ('<screen name="WarderRadioScreenSaver" position="0,0"'
            ' size="1920,1080" zPosition="3000" flags="wfNoBorder"'
            ' backgroundColor="#000000">' + _MARKUP + '</screen>')

    def __init__(self, session):
        Screen.__init__(self, session)
        self._positions = _POSITIONS
        self._offset = (0, 0)
        self._direction = (1, 1)
        self._ticks = 0
        self._last_values = {}
        self._last_picon = None
        self._last_cover = None
        self._picon_ref = None
        self._picon_value = ""
        self._cover_request = None
        self._cover_result = None
        self._cover_running = False
        self._closed = False
        self._ready = False
        for name in self._positions:
            self[name] = Pixmap() if name in ("saver_picon", "saver_cover") else Label("")
        self._timer = eTimer()
        try:
            self._timer_conn = self._timer.timeout.connect(self._refresh)
        except AttributeError:
            self._timer.callback.append(self._refresh)
        self.onLayoutFinish.append(self._layout)
        self.onShow.append(self._show)
        self.onHide.append(self._hide)
        self.onClose.append(self._close)

    def _layout(self):
        self._ready = True

    def _show(self):
        self._closed = False
        self._refresh()
        self._timer.start(1000, False)

    def _hide(self):
        self._timer.stop()

    def _close(self):
        self._closed = True
        self._timer.stop()

    def _label(self, name, value):
        value = str(value or "")
        if self._last_values.get(name) != value:
            self._last_values[name] = value
            self[name].setText(value)

    def _picture(self, name, path):
        if name == "saver_picon":
            cache = "_last_picon"
        else:
            cache = "_last_cover"
        if path == getattr(self, cache):
            return
        setattr(self, cache, path)
        if not path or not os.path.isfile(path):
            self[name].hide()
            return
        try:
            pix = LoadPixmap(path=path)
            if pix is None:
                self[name].hide()
                return
            self[name].instance.setPixmap(pix)
            self[name].show()
        except Exception:
            self[name].hide()

    def _cover_background(self, identity):
        try:
            from .warderRadioCoverSearch import lookup_cover
            path, provider = lookup_cover(identity[0], identity[1])
        except Exception:
            path = ""
        # Worker only publishes a path. GUI widgets are touched by _refresh.
        self._cover_result = (identity, path)
        self._cover_running = False

    def _refresh(self):
        if self._closed or not self._ready:
            return
        try:
            nav = self.session.nav
            ref = nav.getCurrentlyPlayingServiceReference()
            service = nav.getCurrentService()
            if ref is None:
                return
            name = _service_name(ref, service)
            group, kind = _service_group(ref, service)
            if stream_url(ref):
                artist, track = current_song(service, ref)
            else:
                artist, track = native_song(service)
            self._label("saver_head", "RADIO")
            self._label("saver_station", name or "Rádio")
            self._label("saver_group", group)
            self._label("saver_artist_caption", "ARTIST")
            self._label("saver_artist", artist or "—")
            self._label("saver_track_caption", "SONG")
            self._label("saver_track", track or "—")
            self._label("saver_signal", kind)
            self._label("saver_date", time.strftime("%d.%m.%Y"))
            self._label("saver_time", time.strftime("%H:%M:%S"))
            ref_string = ref.toString()
            # Cheap refresh on slow non-GLES boxes. Recheck occasionally so
            # a radio logo downloaded after activation appears automatically.
            if ref_string != self._picon_ref or self._ticks % 10 == 0:
                self._picon_ref = ref_string
                self._picon_value = _picon_path(ref)
            picon = self._picon_value
            self._picture("saver_picon", picon)
            identity = (artist, track) if artist and track else None
            if identity != self._cover_request and not self._cover_running:
                self._cover_request = identity
                self._cover_result = None
                if identity:
                    self._cover_running = True
                    worker = threading.Thread(target=self._cover_background, args=(identity,))
                    worker.daemon = True
                    worker.start()
            cover = (self._cover_result[1]
                     if self._cover_result and self._cover_result[0] == identity
                     else "")
            self._picture("saver_cover", cover or picon)
            self._ticks += 1
            if self._ticks % 2 == 0:
                self._move()
        except Exception:
            # Missing metadata, an optional image provider, or changing service
            # must never stop radio or crash the receiver GUI.
            pass

    def _move(self):
        self._offset, self._direction = bounded_motion(
            self._offset, self._direction)
        dx, dy = self._offset
        for name, (x, y, width, height) in self._positions.items():
            if name == "saver_black":
                continue
            try:
                self[name].instance.move(ePoint(x + dx, y + dy))
            except Exception:
                pass
