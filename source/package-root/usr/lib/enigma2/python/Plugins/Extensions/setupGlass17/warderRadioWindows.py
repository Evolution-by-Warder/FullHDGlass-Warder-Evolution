# -*- coding: utf-8 -*-
"""Radio InfoBar windows must preserve the native RDS framebuffer below."""
from Components.Converter.WarderRadioOnly import is_radio_reference
from Components.Converter.WarderRadioMetadata import current_song, stream_url, monitor
from enigma import eTimer


def _log(value):
    # Runtime diagnostics were retired after the receiver-confirmed test250.
    pass


class RadioWindowTransparency:
    def __init__(self, bar):
        self.bar = bar
        self.original = {}
        self._songTimer = eTimer()
        self._songTimer.callback.append(self.update_song)
        if hasattr(bar, "onClose"):
            bar.onClose.append(self.close)

    def close(self):
        self._songTimer.stop()
        monitor.clear()

    def update_song(self):
        try:
            nav = self.bar.session.nav
            reference = nav.getCurrentlyPlayingServiceReference()
            if not stream_url(reference):
                self.close()
                return
            artist, title = current_song(nav.getCurrentService(), reference)
            display = getattr(self.bar, "rds_display", None)
            if display is not None:
                label = display["RadioText"]
                text = " - ".join(part for part in (artist, title) if part)
                label.setText(text)
                if text:
                    label.show()
        except Exception:
            pass

    def update(self):
        try:
            reference = self.bar.session.nav.getCurrentlyPlayingServiceReference()
            radio = is_radio_reference(reference)
            if stream_url(reference):
                self.update_song()
                self._songTimer.start(1000)
            else:
                self.close()
            for name, screen in (("InfoBar", self.bar),
                                 ("ExtraInfo17", getattr(self.bar, "g17dialog", None))):
                root = getattr(screen, "instance", None)
                if root is None:
                    continue
                record = self.original.get(name)
                if record is None or record[0] is not root:
                    # eWindow owns a separate client eWidget. Both default to
                    # opaque, independently of backgroundColor's alpha value.
                    # Keep the client proxy: SWIG may return a fresh proxy on
                    # each child() call even though it is the same C++ widget.
                    client = root.child()
                    record = (root, client, bool(root.isTransparent()),
                              bool(client.isTransparent()))
                    self.original[name] = record
                root, client, old_root, old_client = record
                before = [bool(root.isTransparent()), bool(client.isTransparent())]
                target = [True, True] if radio else [old_root, old_client]
                for widget, desired in zip((root, client), target):
                    if bool(widget.isTransparent()) != desired:
                        widget.setTransparent(1 if desired else 0)
                after = [bool(root.isTransparent()), bool(client.isTransparent())]
                if before != after:
                    root.invalidate()
                    _log({"event": "window_transparency", "window": name,
                          "radio": radio, "before": before, "after": after})
        except Exception as error:
            _log({"event": "window_transparency_error", "error": repr(error)})


def install_radio_window_transparency(bar):
    controller = getattr(bar, "_warderRadioWindows", None)
    if controller is not None:
        return controller
    controller = RadioWindowTransparency(bar)
    bar._warderRadioWindows = controller
    # Ordinary bound callbacks are supported by Screen.show(). No layout
    # callback or dialog/action replacement is needed.
    bar.onShow.append(controller.update)
    extra = getattr(bar, "g17dialog", None)
    if extra is not None:
        extra.onShow.append(controller.update)
    controller.update()
    return controller

