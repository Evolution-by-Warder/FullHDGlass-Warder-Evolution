# -*- coding: utf-8 -*-
"""Idle-driven saver for every native Enigma2 radio source, never for TV.

Install only on FullHDGlass's InfoBar. Do not change Enigma2 global classes,
the radio plugin's own saver, playback, or the user's channel list.
"""
import time

from enigma import eTimer, eActionMap
from Components.Converter.WarderRadioOnly import is_radio_reference, is_native_dab
from .warderRadioSaverLayout import delay_seconds
from .screenSaver import ScreenSaverScreen

_controller = None


def _is_radio(ref):
    if ref is None:
        return False
    if is_native_dab(ref) or is_radio_reference(ref):
        return True
    # Some images' ServiceReference.isRadioServiceReference does not know
    # IPTV radio (4097/5001) or DAB; service field 2 is the radio marker.
    try:
        fields = ref.toString().split(":")
        return len(fields) > 2 and fields[2].upper() in ("2", "A")
    except Exception:
        return False


class UnifiedRadioSaver:
    def __init__(self, infobar, setting):
        self.infobar = infobar
        self.session = infobar.session
        self.setting = setting
        self.dialog = None
        self.last_activity = time.monotonic()
        self.last_service = None
        self.closed = False
        self.bound = False
        self.native_suspended = False
        self._watch = eTimer()
        try:
            self._watch_conn = self._watch.timeout.connect(self.poll)
        except AttributeError:
            self._watch.callback.append(self.poll)
        self._actions = eActionMap.getInstance()
        # Observe all remote activity without consuming normal actions.
        # Highest priority is needed only to swallow the FIRST wake key.
        try:
            self._actions.bindAction("", -0x7fffffff, self._key)
            self.bound = True
        except Exception:
            # Without key interception a saver might swallow ordinary commands
            # or activate while the user is operating the receiver: stay off.
            self.bound = False
        if self.bound:
            self._watch.start(1000, False)
        if hasattr(infobar, "onClose"):
            infobar.onClose.append(self.close)

    def _key(self, *args):
        if self.closed:
            return 0
        try:
            flag = int(args[-1])
        except (IndexError, ValueError, TypeError):
            flag = 0
        if flag != 0:
            return 1 if self.dialog is not None else 0
        self.last_activity = time.monotonic()
        if self.dialog is not None:
            self._dismiss()
            return 1
        return 0

    def _dismiss(self):
        screen = self.dialog
        if screen is None:
            return
        self.dialog = None
        self.last_activity = time.monotonic()
        try:
            screen.close()
        except Exception:
            pass

    def _closed_dialog(self, *args):
        self.dialog = None
        self.last_activity = time.monotonic()

    def _suspend_native(self):
        # OpenATV can run its own InfoBarScreenSaver for audio services.
        # Temporarily pause only this InfoBar timer while our saver owns radio.
        timer = getattr(self.infobar, "screenSaverTimer", None)
        if timer is None:
            return
        try:
            timer.stop()
            self.native_suspended = True
            native = getattr(self.infobar, "screenSaver", None)
            if native is not None and getattr(native, "shown", False):
                native.hide()
        except Exception:
            pass

    def _restore_native(self, restart=True):
        if not self.native_suspended:
            return
        self.native_suspended = False
        starter = getattr(self.infobar, "screenSaverTimerStart", None)
        if restart and callable(starter):
            try:
                starter()
            except Exception:
                pass

    def _current_ref(self):
        try:
            return self.session.nav.getCurrentlyPlayingServiceReference()
        except Exception:
            return None

    def poll(self):
        if self.closed or not self.bound:
            return
        delay = delay_seconds(self.setting.value)
        ref = self._current_ref()
        try:
            fingerprint = ref.toString() if ref is not None else ""
            radio = _is_radio(ref)
        except Exception:
            fingerprint, radio = "", False
        now = time.monotonic()
        if fingerprint != self.last_service:
            self.last_service = fingerprint
            self.last_activity = now
            # A remote programme switch updates the saver only after a new
            # idle period, never leaves old station data onscreen.
            self._dismiss()
        if not radio or not delay:
            self._dismiss()
            self._restore_native()
            return
        self._suspend_native()
        if self.dialog is not None:
            if self.session.current_dialog is not self.dialog:
                self._dismiss()
            return
        # Channel selection, settings, plugins and modal dialogs must never
        # be covered. The standalone Warder Radio plugin owns its own saver.
        if self.session.current_dialog is not self.infobar:
            self.last_activity = now
            return
        if now - self.last_activity < delay:
            return
        try:
            self.dialog = self.session.openWithCallback(
                self._closed_dialog, ScreenSaverScreen)
        except Exception:
            self.last_activity = now
            self.dialog = None

    def close(self):
        if self.closed:
            return
        self.closed = True
        self._dismiss()
        self._watch.stop()
        self._restore_native(restart=False)
        if self.bound:
            try:
                self._actions.unbindAction("", self._key)
            except Exception:
                pass
            self.bound = False


def install(infobar, setting):
    global _controller
    existing = getattr(infobar, "_warderUnifiedRadioSaver", None)
    if existing is not None:
        return existing
    if _controller is not None:
        _controller.close()
    _controller = UnifiedRadioSaver(infobar, setting)
    infobar._warderUnifiedRadioSaver = _controller
    return _controller
