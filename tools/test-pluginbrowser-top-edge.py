#!/usr/bin/env python3
"""Static regression checks for borderless fullscreen PluginBrowserList."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/hdg17Screens.xml"
text = SKIN.read_text(encoding="utf-8")
start = '<screen name="PluginBrowserList-1"'
assert text.count(start) == 1, "Expected one OpenATV PluginBrowserList template"
screen = text.split(start, 1)[1].split("</screen>", 1)[0]
assert '<screen name="PluginBrowserList-1" position="0,0" size="1920,1080" backgroundColor="background" title="Plugin browser" flags="wfNoBorder">' in text, "Fullscreen PluginBrowser must be borderless"
assert not re.search(r'<eLabel[^>]*position="0,0"[^>]*size="1920,32"', screen), "Obsolete top-edge black masking must not return"
assert re.search(r'<widget source="Title"[^>]*position="98,46"', screen), "Plugin title was moved"
assert re.search(r'<widget source="pluginList"[^>]*position="80,150"', screen), "Plugin list was moved"
assert 'position="80,949"' in screen and 'position="1545,949"' in screen, "Footer positions were changed"
print("PASS: borderless PluginBrowserList, no top-edge mask, approved geometry")
