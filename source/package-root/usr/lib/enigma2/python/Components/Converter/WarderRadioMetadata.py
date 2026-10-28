# -*- coding: utf-8 -*-
"""Shared internet-radio metadata; incomplete pairs carry display-only text. Network reads never run on the GUI thread.

Independent Warder implementation. HDF Radio's metadata/cover feature was the
owner's reference; no compiled HDF modules or station database are redistributed.
"""
import html
import re
import threading
import time
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen


def clean(value):
    return " ".join(re.sub(r"[\x00-\x1f\x7f]", " ", html.unescape(value or "")).split())[:1024]


def split_song(value):
    text = clean(value)
    for separator in (" - ", " – ", " — ", ": "):
        if separator in text:
            artist, title = (part.strip() for part in text.split(separator, 1))
            if artist and title:
                return artist, title
    return "", ""


def stream_url(reference):
    """Only explicit radio services, never TV IPTV or an unrelated web URL."""
    try:
        fields = reference.toString().split(":", 10)
        if len(fields) != 11 or fields[2].upper() not in ("2", "A"):
            return ""
        if fields[0] not in ("4097", "5001", "5002", "8193"):
            return ""
        getter = getattr(reference, "getPath", None)
        value = getter() if callable(getter) else fields[10]
        if value.lower().startswith(("http%3a", "https%3a")):
            value = unquote(value)
        parts = urlsplit(value)
        return value if parts.scheme in ("http", "https") and parts.hostname else ""
    except (AttributeError, TypeError, ValueError):
        return ""


def native_song(service):
    try:
        from enigma import iServiceInformation
        info = service.info() if service else None
        if info is None:
            return "", ""
        def tag(name):
            number = getattr(iServiceInformation, name, None)
            return clean(info.getInfoString(number)) if number is not None else ""
        artist, title = tag("sTagArtist"), tag("sTagTitle")
        if artist and title:
            return artist, title
        parsed = split_song(title)
        return parsed if all(parsed) else (artist, title)
    except Exception:
        return "", ""


def parse_icy(payload):
    try:
        text = payload.rstrip(b"\x00").decode("utf-8")
    except UnicodeDecodeError:
        text = payload.rstrip(b"\x00").decode("cp1252", "replace")
    match = re.search(r"StreamTitle\s*=\s*(['\"])(.*?)\1\s*(?:;|$)", text, re.I | re.S)
    text = clean(match.group(2)) if match else ""
    parsed = split_song(text)
    return parsed if all(parsed) else ("", text)


def fetch_icy(url, opener=urlopen, clock=time.monotonic):
    request = Request(url, headers={"Icy-MetaData": "1", "User-Agent": "FullHDGlass-Warder-Evolution", "Connection": "close"})
    with opener(request, timeout=3.0) as response:
        try:
            interval = int(response.headers.get("icy-metaint", "0"))
        except (ValueError, TypeError):
            return "", ""
        if not 0 < interval <= 256 * 1024:
            return "", ""
        deadline = clock() + 6.0
        def read_exact(count):
            chunks = []
            while count:
                if clock() > deadline:
                    raise TimeoutError("Radio metadata read deadline exceeded")
                chunk = response.read(min(count, 4096))
                if not chunk:
                    raise EOFError("Radio metadata stream ended")
                chunks.append(chunk)
                count -= len(chunk)
            return b"".join(chunks)
        read_exact(interval)
        size = read_exact(1)[0] * 16
        return parse_icy(read_exact(size)) if size else ("", "")


class IcyMonitor:
    """One bounded worker shared by the cover and text, with station ownership."""
    def __init__(self, fetch=fetch_icy, clock=time.monotonic):
        self.fetch, self.clock = fetch, clock
        self.lock = threading.Lock()
        self.url = ""
        self.result = ("", "")
        self.generation = 0
        self.next_check = 0.0
        self.busy = False

    def clear(self):
        with self.lock:
            if self.url:
                self.generation += 1
                self.url, self.result, self.next_check = "", ("", ""), 0.0

    def song(self, url):
        with self.lock:
            if url != self.url:
                self.generation += 1
                self.url, self.result, self.next_check = url, ("", ""), 0.0
            if not self.busy and self.clock() >= self.next_check:
                self.busy = True
                self.next_check = self.clock() + 15.0
                generation = self.generation
                def work():
                    try:
                        result = self.fetch(url)
                    except Exception:
                        result = ("", "")
                    with self.lock:
                        if generation == self.generation and url == self.url:
                            self.result = result
                        self.busy = False
                thread = threading.Thread(target=work, name="WarderRadioMetadata", daemon=True)
                thread.start()
            return self.result


monitor = IcyMonitor()


def current_song(service, reference):
    url = stream_url(reference)
    if not url:
        monitor.clear()
        return "", ""
    artist, title = native_song(service)
    # A standalone native announcement is current metadata too. Do not replace
    # it with a previous song still held by the background ICY monitor.
    if artist or title:
        monitor.clear()
        return artist, title
    return monitor.song(url)
