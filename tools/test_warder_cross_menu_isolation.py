"""Guard that ChannelSelection-only changes do not spread to other menu families.

This is a static source audit, NOT evidence that those menus render correctly.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKINS = (
    ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/hdg17Screens.xml",
    ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml",
)
SCREEN = re.compile(r'<screen\b[^>]*name="([^"]+)"[^>]*>(.*?)</screen>', re.S)
NON_CHANNEL_FAMILIES = ("EPGSelection", "MovieSelection", "EventView", "ChannelSelectionRadio")


def inspected_screens():
    for path in SKINS:
        for name, body in SCREEN.findall(path.read_text(encoding="utf-8")):
            yield path.name, name, body


class CrossMenuIsolationTests(unittest.TestCase):
    def test_other_menu_families_remain_out_of_prime_time_scope(self):
        found = {family: 0 for family in NON_CHANNEL_FAMILIES}
        for filename, name, body in inspected_screens():
            for family in NON_CHANNEL_FAMILIES:
                if name == family or name.startswith(family + "-"):
                    found[family] += 1
                    self.assertNotIn('render="WarderPrimeTime"', body, (filename, name))
                    self.assertNotIn('WarderPrimeTimeGate', body, (filename, name))
        for family, count in found.items():
            self.assertGreater(count, 0, family)

    def test_channel_progress_margin_is_not_applied_to_other_menus(self):
        for filename, name, body in inspected_screens():
            if name == "ChannelSelection" or name.startswith("ChannelSelection-"):
                continue
            for line in body.splitlines():
                if '<widget' in line and 'name="list"' in line:
                    self.assertNotIn('fieldMargins="26"', line, (filename, name))

    def test_only_channel_selection_list_margins_are_affected(self):
        templates = SKINS[0].read_text(encoding="utf-8")
        for name, body in SCREEN.findall(templates):
            if name.startswith("ChannelSelection-"):
                continue
            self.assertNotIn('render="WarderPrimeTime"', body, name)


if __name__ == "__main__":
    unittest.main()
