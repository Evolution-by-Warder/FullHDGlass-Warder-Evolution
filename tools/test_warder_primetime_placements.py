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
    "ChannelSelection-14": ("15,678", "1395,45"),
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
            # Confirm the gate belongs to the *same* EPG cell as the
            # PrimeTime label. A misplaced gate can hide an unrelated item.
            gate_index = body.index('WarderPrimeTimeGate')
            widget_start = body.rfind('<widget', 0, gate_index)
            self.assertGreaterEqual(widget_start, 0, screen_name)
            original_tag = body[widget_start:body.index('>', widget_start) + 1]
            self.assertIn('source="ServiceEvent"', original_tag, screen_name)
            self.assertIn('position="%s"' % position, original_tag, screen_name)
            if screen_name in ("ChannelSelection-1", "ChannelSelection-2", "ChannelSelection-9"):
                self.assertIn('render="g17EmptyEpg"', original_tag, screen_name)
                self.assertIn('warderPrimeTimeGate="1"', original_tag, screen_name)
            original_size = re.search(r'size="(\d+),(\d+)"', original_tag)
            overlay_size = re.search(r'size="(\d+),(\d+)"', overlay)
            self.assertIsNotNone(original_size, screen_name)
            self.assertIsNotNone(overlay_size, screen_name)
            self.assertGreaterEqual(int(original_size[1]), int(overlay_size[1]), screen_name)
            self.assertGreaterEqual(int(original_size[2]), int(overlay_size[2]), screen_name)
            count += 1
        self.assertEqual(count, len(TARGETS))

    def test_fallback_is_explicitly_suppressed_only_in_gated_cells(self):
        renderer = (ROOT / 'source/package-root/usr/lib/enigma2/python/Components/Renderer/g17EmptyEpg.py').read_text(encoding='utf-8')
        self.assertIn('elif attrib == "warderPrimeTimeGate"', renderer)
        self.assertIn('if self.warderPrimeTimeGate:', renderer)
        self.assertIn('self.fillTimer.stop()', renderer)
        self.assertIn('self.lastText = self.backText = ""', renderer)

    def test_empty_epg_text_truncation_is_bounded(self):
        renderer = (ROOT / 'source/package-root/usr/lib/enigma2/python/Components/Renderer/g17EmptyEpg.py').read_text(encoding='utf-8')
        self.assertIn('available_width = max(0, self.sizeX - 30)', renderer)
        self.assertIn('while tmp and text_width > available_width:', renderer)
        self.assertIn('if self.testSizeLabel.calculateSize().width() <= available_width:', renderer)

    def test_empty_epg_clears_stale_typewriter_on_service_reset(self):
        renderer = (ROOT / 'source/package-root/usr/lib/enigma2/python/Components/Renderer/g17EmptyEpg.py').read_text(encoding='utf-8')
        self.assertIn('if what[0] == self.CHANGED_CLEAR:', renderer)
        self.assertIn('self.tt = self.lastText = self.backText = ""', renderer)
        self.assertIn('if ena and tmp:', renderer)

    def test_queued_typewriter_tick_respects_prime_time_gate(self):
        renderer = (ROOT / 'source/package-root/usr/lib/enigma2/python/Components/Renderer/g17EmptyEpg.py').read_text(encoding='utf-8')
        tick = renderer.split('def __fillText(self):', 1)[1].split('def preWidgetRemove', 1)[0]
        self.assertIn('self.fillTimer.stop()', tick)
        self.assertIn('if self.warderPrimeTimeGate:', tick)
        self.assertIn('if config.plugins.warderEvolutionPrimeTime.enabled.value:', tick)
        self.assertLess(tick.index('if self.warderPrimeTimeGate:'), tick.index('self.posIdx += 1'))

    def test_epg_renderers_initialize_optional_service_reference(self):
        base = ROOT / 'source/package-root/usr/lib/enigma2/python/Components/Renderer'
        for name in ('g17ShowExtraEpg.py', 'g17ShowExtEpg.py'):
            renderer = (base / name).read_text(encoding='utf-8')
            self.assertIn('service = None\n\t\t\t\ttry:\n\t\t\t\t\tservice = self.source.service', renderer, name)

    def test_prime_time_renderer_hides_invalid_source_and_clear(self):
        renderer = (ROOT / 'source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderPrimeTime.py').read_text(encoding='utf-8')
        self.assertIn('if not enabled or what[0] == self.CHANGED_CLEAR:', renderer)
        self.assertIn('if service is None:', renderer)
        self.assertIn('eServiceReference.isMarker | eServiceReference.flagDirectory', renderer)
        self.assertIn('except (AttributeError, RuntimeError, TypeError, ValueError):\\n            self.text = ""\\n            self.instance.hide()\\n            return', renderer)

    def test_base_source_is_unchanged_and_no_global_overlay(self):
        content = BASE.read_text(encoding="utf-8")
        self.assertNotIn('WarderPrimeTime', content)
        self.assertNotIn('fieldMargins="26"', content)


if __name__ == "__main__":
    unittest.main()
