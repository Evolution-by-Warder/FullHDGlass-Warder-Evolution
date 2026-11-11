# -*- coding: utf-8 -*-
"""Background I/O for Warder channel picons. Never access Enigma2 widgets here."""
import os
import shutil
import tempfile
import threading
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty


class ChannelWorker(object):
    def __init__(self, job, destination, wanted, fetch, install):
        self.job = dict(job)
        self.destination = destination
        self.wanted = wanted
        self.fetch = fetch
        self.install = install
        self.events = Queue()
        self.thread = threading.Thread(target=self.run, name="WarderChannelDownload")
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def drain(self):
        while True:
            try:
                yield self.events.get_nowait()
            except Empty:
                return

    def run(self):
        archive = None
        try:
            needed = int((int(self.job.get("bytes", 0)) * 2.2) / (1024 * 1024)) + 10
            if int(shutil.disk_usage("/tmp").free / (1024 * 1024)) < needed:
                raise ValueError("insufficient temporary space for Warder channel package")
            if os.path.islink(self.destination) or not os.path.isdir(self.destination):
                raise ValueError("unsafe Warder picon destination")
            if int(shutil.disk_usage(self.destination).free / (1024 * 1024)) < needed:
                raise ValueError("insufficient destination space for Warder channel package")
            fd, archive = tempfile.mkstemp(prefix="warder-channel-", suffix=".zip", dir="/tmp")
            os.close(fd)
            self.events.put(("stage", "Downloading channel package"))
            self.fetch(self.job, archive, lambda done, total: self.events.put(("bytes", (done, total))))
            self.events.put(("stage", "Checking and installing PNG files"))
            installed, available = self.install(archive, self.destination, self.wanted)
            self.events.put(("done", (installed, available)))
        except Exception as error:
            self.events.put(("error", str(error)))
        finally:
            if archive:
                try:
                    os.unlink(archive)
                except OSError:
                    pass


class ManifestWorker(object):
    """Fetch the approved manifest without freezing the GUI event loop."""
    def __init__(self, url, fetch):
        self.url = url
        self.fetch = fetch
        self.events = Queue()
        self.thread = threading.Thread(target=self.run, name="WarderManifestDownload")
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def drain(self):
        while True:
            try:
                yield self.events.get_nowait()
            except Empty:
                return

    def run(self):
        try:
            self.events.put(("done", self.fetch(self.url)))
        except Exception as error:
            self.events.put(("error", str(error)))


class AssetWorker(object):
    """Run a verified archive download/extraction without touching Enigma widgets."""
    def __init__(self, asset, target, work):
        self.asset = dict(asset)
        self.target = target
        self.work = work
        self.events = Queue()
        self.thread = threading.Thread(target=self.run, name="WarderAssetDownload")
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def drain(self):
        while True:
            try:
                yield self.events.get_nowait()
            except Empty:
                return

    def run(self):
        try:
            root = self.work(self.asset, self.target, self.report, self.stage)
            self.events.put(("done", root))
        except Exception as error:
            self.events.put(("error", str(error)))

    def report(self, done, total):
        self.events.put(("bytes", (done, total)))

    def stage(self, label):
        self.events.put(("stage", label))


class LegacyArchiveWorker(object):
    """Fetch and extract one pinned legacy 7z archive without blocking the GUI."""
    _ROOT = ("https://raw.githubusercontent.com/Evolution-by-Warder/Trezor/"
             "9cdda4ab414e7d50a97ca9285db8ebbb75fba615/"
             "archives/chocholousek-picons/originals/")

    def __init__(self, url, destination, sevenzip):
        self.url = str(url)
        self.destination = destination
        self.sevenzip = sevenzip
        self.events = Queue()
        self.thread = threading.Thread(target=self.run, name="WarderLegacyArchive")
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def drain(self):
        while True:
            try:
                yield self.events.get_nowait()
            except Empty:
                return

    def run(self):
        import subprocess
        import time
        try:
            from urllib.request import Request, build_opener, HTTPCookieProcessor
            from http.cookiejar import CookieJar
        except ImportError:
            from urllib2 import Request, build_opener, HTTPCookieProcessor
            from cookielib import CookieJar
        archive = None
        extracted = False
        safe_cleanup = False
        target = None
        try:
            from os.path import basename, realpath, dirname
            if (not self.url.startswith(self._ROOT)
                    or not self.url.endswith(".7z")
                    or basename(self.url) != self.url[len(self._ROOT):]):
                raise ValueError("untrusted preserved legacy archive")
            target = realpath(self.destination)
            if target == "/tmp" or not target.startswith("/tmp/") or target == "/tmp/":
                raise ValueError("invalid legacy extraction path")
            safe_cleanup = True
            if not os.path.isfile(self.sevenzip):
                raise ValueError("missing legacy 7zip helper")
            shutil.rmtree(target, ignore_errors=True)
            fd, archive = tempfile.mkstemp(prefix="warder-legacy-", suffix=".7z", dir="/tmp")
            self.events.put(("stage", "download"))
            received = 0
            last_update = 0.0
            opener = build_opener(HTTPCookieProcessor(CookieJar()))
            req = Request(self.url, headers={"User-Agent": "FHDG17-Warder"})
            with os.fdopen(fd, "wb") as out, opener.open(req, timeout=15) as response:
                if str(response.geturl()) != self.url:
                    raise ValueError("untrusted legacy archive redirect")
                expected = int(response.headers.get("Content-Length") or 0)
                while True:
                    chunk = response.read(1024 * 128)
                    if not chunk:
                        break
                    received += len(chunk)
                    out.write(chunk)
                    now = time.monotonic()
                    if now - last_update >= 0.25:
                        self.events.put(("bytes", (received, expected)))
                        last_update = now
            if received < 1:
                raise ValueError("empty legacy archive")
            self.events.put(("bytes", (received, expected)))
            needed = (received * 2.0)
            if shutil.disk_usage("/tmp").free < needed:
                raise ValueError("insufficient space to extract legacy archive")
            os.makedirs(target, exist_ok=True)
            self.events.put(("stage", "extract"))
            with open(os.devnull, "wb") as devnull:
                result = subprocess.call(
                    [self.sevenzip, "e", "-y", "-bd", "-o%s" % target, archive],
                    stdout=devnull, stderr=devnull)
            if result:
                raise ValueError("legacy archive extraction failed")
            extracted = True
            self.events.put(("done", received))
        except Exception as error:
            self.events.put(("error", str(error)))
        finally:
            if archive:
                try:
                    os.unlink(archive)
                except OSError:
                    pass
            if not extracted and safe_cleanup:
                shutil.rmtree(target, ignore_errors=True)
