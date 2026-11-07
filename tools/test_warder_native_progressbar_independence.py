"""Source-level regression for native Enigma2 progressbar event independence."""
from pathlib import Path
import importlib.util
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/apply-native-progressbar-event-fix.py"
RENDERER = ROOT / "source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderChannelEpgClip.py"


def load_patch():
    spec = importlib.util.spec_from_file_location("native_progress_fix", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.patch


class NativeProgressbarIndependenceTests(unittest.TestCase):
    def test_native_patch_preserves_paint_branch_and_adds_event_lookup(self):
        old = (
            "\t\teRect area = m_element_position[celServiceEventProgressbar];\n"
            "\t\tif (area.width() > 0 && evt && !m_element_font[celServiceEventProgressbar])\n"
            "\t\t{\n"
        )
        fixed = load_patch()(old)
        self.assertIn("area.width() > 0 && !evt && isPlayable && service_info", fixed)
        self.assertIn("service_info->getEvent(*m_cursor, evt);", fixed)
        self.assertIn("if (area.width() > 0 && evt && !m_element_font[celServiceEventProgressbar])", fixed)
        self.assertEqual(fixed.count("getEvent(*m_cursor, evt)"), 1)
        with self.assertRaisesRegex(RuntimeError, "Expected exactly one"):
            load_patch()(fixed)

    def test_missing_or_duplicated_source_anchor_aborts_without_modification(self):
        with self.assertRaisesRegex(RuntimeError, "Expected exactly one"):
            load_patch()("unrelated C++ text")
        anchor = ("  eRect area = m_element_position[celServiceEventProgressbar];\n"
                  "  if (area.width() > 0 && evt && !m_element_font[celServiceEventProgressbar])")
        with self.assertRaisesRegex(RuntimeError, "found 2"):
            load_patch()(anchor + "\n" + anchor)

    def test_renderer_never_paints_native_progressbars_or_text_masks(self):
        text = RENDERER.read_text(encoding="utf-8")
        self.assertIn("setElementFont(component.l.celServiceInfo, None)", text)
        self.assertNotIn("self._draw_progress(", text)
        self.assertNotIn("_opaque_black", text)
        self.assertNotIn('gFont("Regular", 1)', text)


if __name__ == "__main__":
    unittest.main()
