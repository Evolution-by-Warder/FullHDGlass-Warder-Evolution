"""Verify the native Enigma2 fix which unblocks real progressbars with no text mask.

This is source-contract validation only. A receiver must boot a compiled
Enigma2 containing the patch before native bar-mode QA can pass.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "compatibility/native-enigma2-patches/0001-progressbar-event-independent-of-epg-font.patch"
RENDERER = ROOT / "source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderChannelEpgClip.py"


class NativeProgressbarIndependenceTests(unittest.TestCase):
    def test_patch_fetches_event_only_for_native_bar_when_text_cell_disabled(self):
        patch = PATCH.read_text(encoding="utf-8")
        self.assertIn("lib/service/listboxservice.cpp", patch)
        self.assertIn("area.width() > 0 && !evt && !m_element_font[celServiceEventProgressbar]", patch)
        self.assertIn("&& isPlayable && service_info", patch)
        self.assertIn("service_info->getEvent(*m_cursor, evt);", patch)
        self.assertIn("if (area.width() > 0 && evt && !m_element_font[celServiceEventProgressbar])", patch)
        self.assertNotIn("painter.fill(", patch)
        self.assertNotIn("painter.blit(", patch)

    def test_renderer_never_paints_progressbars_or_black_text_masks(self):
        source = RENDERER.read_text(encoding="utf-8")
        self.assertIn("setElementFont(component.l.celServiceInfo, None)", source)
        self.assertNotIn("self._draw_progress(", source)
        self.assertNotIn("_opaque_black", source)
        self.assertNotIn('gFont("Regular", 1)', source)


if __name__ == "__main__":
    unittest.main()
