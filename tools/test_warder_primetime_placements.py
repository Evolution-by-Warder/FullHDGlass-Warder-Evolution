"""Regression guard for the 13 alternate layouts using a gated EPG cell.

No screenshots/receiver UI implied: this statically verifies source placement.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKINS = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/hdg17Screens.xml"
BASE = ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml"
SCREEN = re.compile(r'<screen\b[^>]*name="(ChannelSelection-[^"]+)"[^>]*>(.*?)</screen>', re.S)
TARGETS = {
    "ChannelSelection-1": ("189,205", "618,33"),
    "ChannelSelection-2": ("262,864", "690,33"),
    "ChannelSelection-3": ("189,427", "618,33"),
    "ChannelSelection-4": ("262,864", "690,33"),
    "ChannelSelection-6": ("189,427", "618,33"),
    "ChannelSelection-8": ("258,559", "684,33"),
    "ChannelSelection-9": ("352,865", "465,30"),
    "ChannelSelection-10": ("1162,864", "690,33"),
    "ChannelSelection-11": ("1288,742", "474,33"),
    "ChannelSelection-12": ("15,633", "690,33"),
    "ChannelSelection-13": ("225,540", "720,45"),
    "ChannelSelection-14": ("15,678", "1395,195"),
    "ChannelSelection-18": ("225,540", "720,45"),
}


class LayoutTests(unittest.TestCase):
    def test_thirteen_gated_cells_match_original_coordinates(self):
        content = SKINS.read_text(encoding="utf-8")
        count = 0
        for screen_name, body in SCREEN.findall(content):
            if screen_name not in TARGETS:
                self.assertNotIn('render="WarderPrimeTime"', body, screen_name)
                continue
            position, size = TARGETS[screen_name]
            overlays = re.findall(r'<widget\b[^>]*render="WarderPrimeTime"[^>]*/>', body)
            self.assertEqual(len(overlays), 1, screen_name)
            overlay = overlays[0]
            self.assertIn('position="%s"' % position, overlay, screen_name)
            self.assertIn('size="%s"' % size, overlay, screen_name)
            self.assertIn('transparent="1"', overlay, screen_name)
            self.assertIn('noWrap="1"', overlay, screen_name)
            self.assertEqual(body.count('WarderPrimeTimeGate'), 1, screen_name)
            gated = re.findall(r'<widget\b[^>]*>[\s\S]*?WarderPrimeTimeGate[\s\S]*?</widget>', body)
            # The original service EPG widget must be gated, not the list.
            self.assertTrue(any('source="ServiceEvent"' in candidate for candidate in gated), screen_name)
            count += 1
        self.assertEqual(count, len(TARGETS))

    def test_base_source_is_unchanged_and_no_global_overlay(self):
        content = BASE.read_text(encoding="utf-8")
        self.assertNotIn('WarderPrimeTime', content)
        self.assertNotIn('fieldMargins="26"', content)


if __name__ == "__main__":
    unittest.main()
