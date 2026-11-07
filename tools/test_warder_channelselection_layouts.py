"""Static regression guard for all bundled channel-selection variants.

Usage from repository root: python3 tools/test_warder_channelselection_layouts.py
This validates XML source geometry policy, not actual receiver graphics.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/hdg17Screens.xml",
    ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml",
)
SCREEN = re.compile(r'<screen\b[^>]*name="(ChannelSelection(?:-[^"]+)?)"[^>]*>(.*?)</screen>', re.S)
LIST = re.compile(r'<widget\b[^>]*name="list"[^>]*/>', re.S)


class ChannelSelectionLayoutTests(unittest.TestCase):
    def test_all_progressbar_lists_reserve_gap(self):
        seen, checked = set(), 0
        for path in FILES:
            text = path.read_text(encoding="utf-8")
            for name, body in SCREEN.findall(text):
                for widget in LIST.findall(body):
                    if 'picServiceEventProgressbar=' not in widget:
                        continue
                    if path.name == 'skin.xml':
                        self.assertNotIn('fieldMargins="26"', widget, (name, str(path)))
                    else:
                        self.assertIn('fieldMargins="26"', widget, (name, str(path)))
                    checked += 1
                    seen.add(name)
        self.assertEqual(checked, 58)
        self.assertEqual(len(seen), 58)

    def test_runtime_hook_guards_approved_skin_xml(self):
        plugin = (ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py').read_text(encoding='utf-8')
        self.assertIn('if \'picServiceEventProgressbar=\' in line and \'fieldMargins=\' not in line:', plugin)
        self.assertIn('line = line.replace(\'/>\', \' fieldMargins="26" />\')', plugin)

    def test_dual_epg_panels_keep_independent_sources_and_coordinates(self):
        """Seven pre-existing dual panels use playing vs cursor service independently."""
        source = FILES[0].read_text(encoding="utf-8")
        screens = dict(SCREEN.findall(source))
        expected = ("ChannelSelection-1", "ChannelSelection-2", "ChannelSelection-9",
                    "ChannelSelection-31", "ChannelSelection-32",
                    "ChannelSelection-48", "ChannelSelection-a48")
        import xml.etree.ElementTree as ET
        for name in expected:
            root = ET.fromstring('<screen>' + screens[name] + '</screen>')
            widgets = root.findall("widget")
            upper = [w for w in widgets if w.get("source") in
                     ("session.CurrentService", "session.Event_Now", "session.Event_Next")]
            lower = [w for w in widgets if w.get("source") == "ServiceEvent"]
            self.assertTrue(upper, name)
            self.assertTrue(lower, name)
            upper_logos = [w for w in upper if w.get("render") == "g17PicRef"]
            lower_logos = [w for w in lower if w.get("render") == "g17RefTV"]
            self.assertEqual(len(upper_logos), 1, name)
            self.assertEqual(len(lower_logos), 1, name)
            # Upper EPG must not accidentally depend on cursor-selected ServiceEvent.
            self.assertTrue(
                any(w.get("source") == "session.Event_Now"
                    or (w.get("source") == "session.CurrentService"
                        and w.get("render") == "g17ShowExtraEpg") for w in upper),
                name)
            # Preserve original positions instead of moving EPG to another panel.
            for w in upper_logos + lower_logos:
                self.assertIn("position", w.attrib, name)
                self.assertIn("size", w.attrib, name)

    def test_no_font_or_row_height_policy_changed_by_fix(self):
        for path in FILES:
            text = path.read_text(encoding="utf-8")
            for name, body in SCREEN.findall(text):
                for widget in LIST.findall(body):
                    if 'picServiceEventProgressbar=' in widget:
                        self.assertIn("serviceNameFont=", widget, name)
                        self.assertIn("serviceInfoFont=", widget, name)


if __name__ == "__main__":
    unittest.main()
