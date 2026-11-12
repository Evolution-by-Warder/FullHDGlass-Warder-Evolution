#!/usr/bin/env python3
"""Guard the classic full-screen channel list without touching other list types."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ledger = json.loads((ROOT / "design/classic-channel-fullscreen-20261112/layout.json").read_text())
original = ledger["original"]
updated = ledger["updated"]
path = ROOT / ledger["path"]
current = path.read_text()
assert current.count(updated) == 1, "Classic channel screen changed unexpectedly"
assert current.count(original) == 0, "Old compact geometry must not remain"
restored = current.replace(updated, original, 1).encode()
blob_header = b"blob " + str(len(restored)).encode() + b"\0"
assert hashlib.sha1(blob_header + restored).hexdigest() == ledger["baseline_blob_sha"], (
    "A different channel-list variant or unrelated screen was modified")

screen = ET.fromstring(updated)
assert screen.get("name") == "ChannelSelection-12"
assert screen.get("position") == "0,0"
assert screen.get("size") == "1920,1080"
assert screen.get("flags") == "wfNoBorder"
assert screen.find("widget[@source='Title']") is not None

widgets = {w.get("name"): w for w in screen.findall("widget") if w.get("name")}
for name in ("list", "key_red", "key_green", "key_yellow", "key_blue"):
    assert name in widgets, name
listing = widgets["list"]
x, y = map(int, listing.get("position").split(","))
w, h = map(int, listing.get("size").split(","))
pitch = int(listing.get("serviceItemHeight"))
name_font = int(listing.get("serviceNameFont").rsplit(";", 1)[1])
event_font = int(listing.get("serviceInfoFont").rsplit(";", 1)[1])
assert x <= 80 and w >= 1700, "List must use almost all the FullHD width"
assert y >= 200 and y + h <= 840, "List must remain clear of controls/footer"
assert pitch >= max(name_font, event_font) + 12, "Fonts need vertical breathing room"
assert h % pitch == 0, "No partially clipped list row"
assert listing.get("picServiceEventProgressbar")
assert listing.get("fieldMargins") == "26"

for element in screen.iter():
    if element is screen or not element.get("position") or not element.get("size"):
        continue
    ax, ay = map(int, element.get("position").split(","))
    aw, ah = map(int, element.get("size").split(","))
    assert min(ax, ay, aw, ah) >= 0
    assert ax + aw <= 1920 and ay + ah <= 1080, (
        element.tag, element.get("name"), element.get("position"), element.get("size"))
for colour in ("red", "green", "yellow", "blue"):
    key = widgets["key_" + colour]
    kx = int(key.get("position").split(",")[0])
    kw = int(key.get("size").split(",")[0])
    assert 60 <= kx and kx + kw <= 1860

footer = [w for w in screen.findall("widget") if w.get("source") == "ServiceEvent"]
assert len(footer) >= 6, "Do not remove native event, progress, time or name components"
assert any(w.get("render") == "Progress" for w in footer)
assert any(w.get("render") == "g17MetrixHDRunningText" for w in footer)
assert any(w.get("render") == "WarderPrimeTime" for w in footer)
assert any(w.get("render") == "Pixmap" and w.get("source") == "session.CurrentService"
           for w in screen.findall("widget")), "Radio background must remain available"
print("PASS: type12 fullscreen and line pitch, unmodified other 56 variants, footer retained")
