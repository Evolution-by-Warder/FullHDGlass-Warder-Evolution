#!/usr/bin/env python3
"""Static guard for the receiver-test PluginBrowserList top-edge opaque overlay."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/hdg17Screens.xml"
text = SKIN.read_text(encoding="utf-8")
start = '<screen name="PluginBrowserList-1"'
assert text.count(start) == 1, "Expected one OpenATV PluginBrowserList template"
screen = text.split(start, 1)[1].split("</screen>", 1)[0]
mask = '<eLabel position="0,0" size="1920,32" backgroundColor="#00000000" zPosition="10" transparent="0" />'
assert screen.count(mask) == 1, "Missing or duplicate targeted top-edge mask"
assert re.search(r'<widget source="Title"[^>]*position="98,46"', screen), "Plugin title was moved"
assert re.search(r'<widget source="pluginList"[^>]*position="80,150"', screen), "Plugin list was moved"
assert 'position="80,949"' in screen and 'position="1545,949"' in screen, "Footer positions were changed"
assert screen.index(mask) < screen.index('<widget source="pluginList"'), "Cover must be declared before screen content"
assert text.count(mask) == 1, "Mask must not be injected into unrelated screens"
print("PASS: PluginBrowserList top-edge guard and approved geometry")
