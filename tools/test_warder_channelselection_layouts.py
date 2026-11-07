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

    def test_playing_service_epg_visible_on_black_background(self):
        """Playing-service text must remain visible independently of cursor EPG."""
        templates = FILES[0].read_text(encoding="utf-8")
        screens = dict(SCREEN.findall(templates))
        widgets = re.compile(r'<widget\\b[^>]*source="session\\.(?:CurrentService|Event_Now)"[^>]*>', re.S)
        for name in ("ChannelSelection-1", "ChannelSelection-2", "ChannelSelection-9"):
            self.assertIn(name, screens)
            labels = [
                tag for tag in widgets.findall(screens[name])
                if 'render="Label"' in tag or 'render="g17EmptyEpg"' in tag
            ]
            self.assertEqual(len(labels), 4, name)
            for tag in labels:
                self.assertIn('foregroundColor="#ffffff"', tag, (name, tag))
            self.assertIn('source="session.Event_Next"', screens[name])
            self.assertIn('source="ServiceEvent"', screens[name])


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
