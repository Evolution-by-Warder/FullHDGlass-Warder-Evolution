from __future__ import absolute_import

import hashlib
import json
import os
import threading
import unicodedata
try:
    from urllib.parse import quote
    from urllib.request import Request, urlopen
except ImportError:
    from urllib import quote
    from urllib2 import Request, urlopen

from enigma import ePicLoad, ePixmap, eTimer, iRdsDecoder
from Components.Renderer.Renderer import Renderer
import NavigationInstance


class WarderRadioArtwork(Renderer):
    """Exact current-song artwork without modifying OpenATV RdsInfoDisplay."""
    GUI_WIDGET = ePixmap

    def __init__(self):
        Renderer.__init__(self)
        self._key = ""
        self._result = None
        self._busy = False
        self._picload = None
        self._timer = eTimer()
        self._timer.callback.append(self._poll)

    def postWidgetCreate(self, instance):
        Renderer.postWidgetCreate(self, instance)
        instance.hide()
        self._timer.start(1200, False)

    def preWidgetRemove(self, instance):
        try:
            self._timer.stop()
        except Exception:
            pass
        Renderer.preWidgetRemove(self, instance)

    def changed(self, what):
        if self.instance is not None and not self._timer.isActive():
            self._timer.start(1200, False)

    @staticmethod
    def _norm(value):
        try:
            value = unicodedata.normalize("NFKC", value or "")
        except Exception:
            value = value or ""
        try:
            value = value.casefold()
        except Exception:
            value = value.lower()
        return " ".join(value.split())

    @staticmethod
    def _split(text):
        text = (text or "").strip()
        for sep in (" - ", " – ", " — "):
            if sep in text:
                artist, title = text.split(sep, 1)
                if artist.strip() and title.strip():
                    return artist.strip(), title.strip()
        return "", ""

    def _radioText(self):
        try:
            nav = NavigationInstance.instance
            service = nav and nav.getCurrentService()
            decoder = service and service.rdsDecoder()
            return decoder and decoder.getText(iRdsDecoder.RadioText) or ""
        except Exception:
            return ""

    @staticmethod
    def _cacheDir():
        path = "/tmp/warder-radio-artwork"
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
        except Exception:
            pass
        return path

    @classmethod
    def _lookupExact(cls, artist, title, key):
        url = "https://itunes.apple.com/search?entity=song&limit=10&term=" + quote((artist + " " + title).encode("utf-8") if not isinstance(artist, str) else artist + " " + title)
        req = Request(url, headers={"User-Agent": "FullHDGlass17-Warder-Evolution/1.0"})
        raw = urlopen(req, timeout=2.5).read()
        if not isinstance(raw, str):
            raw = raw.decode("utf-8", "replace")
        wantArtist, wantTitle = cls._norm(artist), cls._norm(title)
        for item in json.loads(raw).get("results", []):
            if cls._norm(item.get("artistName")) != wantArtist or cls._norm(item.get("trackName")) != wantTitle:
                continue
            art = (item.get("artworkUrl100") or "").replace("100x100bb", "600x600bb")
            if not art:
                return ""
            path = os.path.join(cls._cacheDir(), hashlib.sha1(key.encode("utf-8")).hexdigest() + ".jpg")
            if not os.path.isfile(path):
                payload = urlopen(Request(art, headers={"User-Agent": "FullHDGlass17-Warder-Evolution/1.0"}), timeout=2.5).read()
                if not payload or len(payload) <= 1024 or payload[:2] != b"\\xff\\xd8":
                    return ""
                tmp = path + ".tmp"
                with open(tmp, "wb") as out:
                    out.write(payload)
                os.rename(tmp, path)
            return path
        return ""

    def _request(self, artist, title, key):
        self._busy = True
        self._result = None
        def worker():
            path = ""
            try:
                cached = os.path.join(self._cacheDir(), hashlib.sha1(key.encode("utf-8")).hexdigest() + ".jpg")
                path = cached if os.path.isfile(cached) else self._lookupExact(artist, title, key)
            except Exception:
                path = ""
            self._result = (key, path)
            self._busy = False
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    def _showPath(self, path):
        if not self.instance or not path or not os.path.isfile(path):
            if self.instance:
                self.instance.hide()
            return
        size = self.instance.size()
        self._picload = ePicLoad()
        self._picload.PictureData.get().append(self._decoded)
        self._picload.setPara((size.width(), size.height(), 1, 1, False, 1, "#00000000"))
        if self._picload.startDecode(path) != 0:
            self._picload = None
            self.instance.hide()

    def _decoded(self, info=None):
        if self._picload and self.instance:
            ptr = self._picload.getData()
            if ptr is not None:
                self.instance.setPixmap(ptr)
                self.instance.show()
        self._picload = None

    def _poll(self):
        if self._result is not None:
            key, path = self._result
            self._result = None
            if key == self._key:
                self._showPath(path)
        artist, title = self._split(self._radioText())
        key = self._norm(artist) + "|" + self._norm(title) if artist and title else ""
        if key != self._key:
            self._key = key
            if self.instance:
                self.instance.hide()
            if key and not self._busy:
                self._request(artist, title, key)
        self._timer.start(1200, False)
