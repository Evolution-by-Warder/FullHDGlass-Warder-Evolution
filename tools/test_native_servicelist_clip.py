"""TEST: OpenATV native event-only clipping is minimal and fail-closed.

Static C++ source validation. It does not prove ARM compilation or receiver QA.
"""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/apply-native-servicelist-clip.py"
spec = importlib.util.spec_from_file_location("nativeclip", TOOL)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

FIXTURE = (
    "void eListboxServiceContent::paint(gPainter &painter) {\n"
    "\tpainter.clip(eRect(offset, m_itemsize));\n"
    "\tcase celServiceInfo:\n"
    "\tm_element_position[celServiceInfo].setLeft(area.left());\n"
    "\tconst int progress = celServiceEventProgressbar;\n"
    "\t\t\t\tpainter.renderPara(para, offset+ePoint(xoffs, yoffs));\n"
    "}\n"
)


class NativeClipSourceTests(unittest.TestCase):
    def test_text_only_is_clipped_while_native_modes_are_untouched(self):
        output = module.patch(FIXTURE)
        self.assertIn("if (e == celServiceInfo)", output)
        self.assertIn("painter.clip(eventClip);", output)
        self.assertIn("painter.clippop();", output)
        self.assertIn("eventClip.setRight(progressArea.left() - m_items_distances)", output)
        self.assertIn("else\n\t\t\t\t\tpainter.renderPara(para, offset+ePoint(xoffs, yoffs));", output)
        self.assertEqual(output.count("Clip only the legacy EPG event label"), 1)
        self.assertEqual(output.count("painter.renderPara(para, offset+ePoint(xoffs, yoffs));"), 2)
        # No mutation to the native bar's event lookup or painter:
        self.assertNotIn("setElementFont", output)
        self.assertNotIn("service_info->getEvent", module.PATCH)
        self.assertNotIn("painter.fill(", module.PATCH)

    def test_repeated_patch_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "anchor"):
            module.patch(module.patch(FIXTURE))

    def test_unknown_source_refuses_to_modify(self):
        with self.assertRaisesRegex(RuntimeError, "anchor"):
            module.patch("unknown C++ source")
        with self.assertRaisesRegex(RuntimeError, "exactly one"):
            module.patch(FIXTURE + module.ANCHOR)

    def test_right_bar_and_percentage_share_same_native_event_clip(self):
        # Width is reserved by ServiceListLegacy for bar, percent and minutes
        # through celServiceEventProgressbar; the fix is mode-neutral.
        for mode in ("barright", "percright", "minsright"):
            with self.subTest(mode=mode):
                output = module.patch(FIXTURE)
                self.assertIn("m_element_position[celServiceEventProgressbar]", output)
                self.assertNotIn('"' + mode + '"', module.PATCH)

    def test_left_side_does_not_clip_to_left_progress_edge(self):
        self.assertIn("progressArea.left() > eventClip.left()", module.PATCH)
        self.assertIn("if (eventClip.width() > 0 && eventClip.height() > 0)", module.PATCH)


if __name__ == "__main__":
    unittest.main()
