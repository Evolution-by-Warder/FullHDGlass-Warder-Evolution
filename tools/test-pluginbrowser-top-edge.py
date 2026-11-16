#!/usr/bin/env python3
"""Check borderless PluginBrowserList and unchanged approved geometry."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/hdg17Screens.xml"
text = SKIN.read_text(encoding="utf-8")
start = '<screen name="PluginBrowserList-1"'
assert text.count(start) == 1
screen = text.split(start, 1)[1].split("</screen>", 1)[0]
assert '<screen name="PluginBrowserList-1" position="0,0" size="1920,1080" backgroundColor="background" title="Plugin browser" flags="wfNoBorder">' in text
assert not re.search(r'<eLabel[^>]*position="0,0"[^>]*size="1920,32"', screen)
assert re.search(r'<widget source="Title"[^>]*position="98,46"', screen)
assert re.search(r'<widget source="pluginList"[^>]*position="80,150"', screen)
assert 'position="80,949"' in screen and 'position="1545,949"' in screen
print("PASS: borderless PluginBrowserList, no masking, approved geometry")
