from __future__ import absolute_import

import hashlib
import json
import os
import threading
import time
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
        self._requestedKey = ""
        self._result = None
        self._busy = False
        self._picload = None
        self._timer = eTimer()
        self._timer.callback.append(self._poll)
        self._diagStart = None
        self._diagService = False
        self._diagRadio = False
        self._diagSong = False

    def postWidgetCreate(self, instance):
        Renderer.postWidgetCreate(self, instance)
        instance.hide()
        self._diagStart = time.time()
        try:
            with open("/tmp/warder-radio-start", "r") as src:
                buttonStart = float(src.read().strip())
            if 0.0 <= self._diagStart - buttonStart <= 30.0:
                self._diagStart = buttonStart
        except Exception:
            pass
        self._diag("RENDERER_START epoch=%.6f t=%.3f" % (time.time(), self._elapsed()))
        # Fast acquisition on RADIO entry; settle to a light poll once metadata is present.
        self._timer.start(100, True)

    def preWidgetRemove(self, instance):
        try:
            self._timer.stop()
        except Exception:
            pass
        Renderer.preWidgetRemove(self, instance)

    def changed(self, what):
        if self.instance is not None and not self._timer.isActive():
            self._timer.start(100, True)

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

    @classmethod
    def _titleCommaIdentity(cls, value):
        # Receiver-proven metadata compatibility only: commas may be omitted by RDS.
        # No other punctuation, suffix, word, or version information is removed.
        return cls._norm(value).replace(",", "")

    @classmethod
    def _artistIdentity(cls, value):
        # TEST173: moderately relax station-vs-catalogue artist separators.
        # Treat common collaboration separators as equivalent, but keep every
        # artist token: this must not turn a partial artist match into a hit.
        value = cls._norm(value)
        for marker in (" feat. ", " feat ", " featuring ", " ft. ", " ft ", " with ", " x ", " / ", " & ", " and "):
            value = value.replace(marker, " | ")
        return tuple(sorted(x.strip(" .,-") for x in value.split("|") if x.strip(" .,-")))

    @classmethod
    def _featIdentity(cls, artist, title):
        artistNorm, titleNorm = cls._norm(artist), cls._norm(title)
        marker = " feat. "
        if marker in artistNorm:
            main, guest = artistNorm.split(marker, 1)
            return main.strip(), titleNorm, guest.strip()
        suffix = " (feat. "
        if suffix in titleNorm and titleNorm.endswith(")"):
            base, guest = titleNorm.rsplit(suffix, 1)
            return artistNorm, base.strip(), guest[:-1].strip()
        return "", "", ""

    @staticmethod
    def _split(text):
        text = (text or "").strip()
        for sep in (" - ", " – ", " — ", ": "):
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

    def _elapsed(self):
        return max(0.0, time.time() - self._diagStart) if self._diagStart is not None else 0.0

    @staticmethod
    def _diag(message):
        try:
            with open("/tmp/warder-radio-artwork.log", "a") as out:
                out.write(message + "\n")
        except Exception:
            pass

    @classmethod
    def _lookupExact(cls, artist, title, key):
        url = "https://itunes.apple.com/search?entity=song&limit=10&term=" + quote((artist + " " + title).encode("utf-8") if not isinstance(artist, str) else artist + " " + title)
        req = Request(url, headers={"User-Agent": "FullHDGlass17-Warder-Evolution/1.0"})
        raw = urlopen(req, timeout=2.5).read()
        if not isinstance(raw, str):
            raw = raw.decode("utf-8", "replace")
        wantArtist, wantTitle = cls._norm(artist), cls._norm(title)
        results = json.loads(raw).get("results", [])
        cls._diag("LOOKUP artist=%r title=%r results=%d" % (artist, title, len(results)))
        for item in results:
            gotArtist, gotTitle = cls._norm(item.get("artistName")), cls._norm(item.get("trackName"))
            exact = gotArtist == wantArtist and gotTitle == wantTitle
            sameArtist = gotArtist == wantArtist or cls._artistIdentity(item.get("artistName")) == cls._artistIdentity(artist)
            if not exact and sameArtist:
                exact = cls._titleCommaIdentity(item.get("trackName")) == cls._titleCommaIdentity(title)
            if not exact:
                wantFeat = cls._featIdentity(artist, title)
                gotFeat = cls._featIdentity(item.get("artistName"), item.get("trackName"))
                exact = bool(wantFeat[0] and wantFeat == gotFeat)
            if not exact:
                cls._diag("REJECT artist=%r title=%r" % (item.get("artistName"), item.get("trackName")))
                continue
            cls._diag("EXACT artist=%r title=%r" % (item.get("artistName"), item.get("trackName")))
            art = (item.get("artworkUrl100") or "").replace("100x100bb", "600x600bb")
            if not art:
                return ""
            path = os.path.join(cls._cacheDir(), hashlib.sha1(key.encode("utf-8")).hexdigest() + ".jpg")
            if not os.path.isfile(path):
                payload = urlopen(Request(art, headers={"User-Agent": "FullHDGlass17-Warder-Evolution/1.0"}), timeout=2.5).read()
                if not payload or len(payload) <= 1024 or not payload.startswith(bytes((255, 216))):
                    return ""
                tmp = path + ".tmp"
                with open(tmp, "wb") as out:
                    out.write(payload)
                os.rename(tmp, path)
            cls._diag("READY path=%s" % path)
            return path
        cls._diag("NO_EXACT artist=%r title=%r" % (artist, title))
        return ""

    def _request(self, artist, title, key):
        self._busy = True
        self._result = None
        def worker():
            path = ""
            try:
                cached = os.path.join(self._cacheDir(), hashlib.sha1(key.encode("utf-8")).hexdigest() + ".jpg")
                path = cached if os.path.isfile(cached) else self._lookupExact(artist, title, key)
            except Exception as err:
                self._diag("ERROR %s: %s" % (err.__class__.__name__, err))
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
        # TEST172: decode into the wider/lower skin box; preserve receiver-proven aspect handling.\n        self._picload.setPara((size.width(), size.height(), 1, 1, False, 1, "#00000000"))
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
        try:
            nav = NavigationInstance.instance
            service = nav and nav.getCurrentService()
        except Exception:
            service = None
        if service is not None and not self._diagService:
            self._diagService = True
            self._diag("SERVICE epoch=%.6f t=%.3f" % (time.time(), self._elapsed()))
        radioText = self._radioText()
        if radioText and not self._diagRadio:
            self._diagRadio = True
            self._diag("RADIOTEXT epoch=%.6f t=%.3f text=%r" % (time.time(), self._elapsed(), radioText))
        artist, title = self._split(radioText)
        if artist and title and not self._diagSong:
            self._diagSong = True
            self._diag("SONG epoch=%.6f t=%.3f artist=%r title=%r" % (time.time(), self._elapsed(), artist, title))
        key = self._norm(artist) + "|" + self._norm(title) if artist and title else ""
        if key != self._key:
            self._key = key
            if self.instance:
                self.instance.hide()
        if not key:
            self._requestedKey = ""
        elif not self._busy and key != self._requestedKey:
            self._requestedKey = key
            self._diag("REQUEST epoch=%.6f t=%.3f artist=%r title=%r" % (time.time(), self._elapsed(), artist, title))
            self._request(artist, title, key)
        self._timer.start(250 if not key else 750, True)
