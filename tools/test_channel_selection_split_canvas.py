"""TEST8: verify split text/bar painting reduces native calls without
changing any eCanvas rectangles or losing backward-compatible fallback.
These mock tests are NOT a receiver-side visual acceptance test.
"""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_warder_channel_epg_clip import ClippedEventTests, Canvas


class SplitCanvasTests(unittest.TestCase):
    def make(self, split=True):
        case = ClippedEventTests(methodName="test_titles_never_reach_reserved_progress_column")
        case.setUp()
        case.renderer._bar_canvas = Canvas() if split else None
        case.renderer._bar_last = None
        case.renderer._perf_bar_skips = 0
        case.renderer._progress_paint_cache = {}
        return case

    def test_first_draw_is_split_into_same_original_text_and_progress_pixels(self):
        original = self.make(False)
        split = self.make(True)
        self.assertTrue(original.draw())
        self.assertTrue(split.draw())
        baseline = original.renderer.instance.calls
        self.assertEqual([x for x in baseline if x[0] == "write"],
                         [x for x in split.renderer.instance.calls if x[0] == "write"])
        self.assertEqual([x for x in baseline if x[0] == "fill"],
                         [x for x in split.renderer._bar_canvas.calls if x[0] == "fill"])
        self.assertEqual(sum(x[0] == "fill" for x in split.renderer.instance.calls), 0)
        self.assertEqual(sum(x[0] == "write" for x in split.renderer._bar_canvas.calls), 0)

    def test_change_of_selected_row_does_not_repaint_static_bars(self):
        case = self.make()
        self.assertTrue(case.draw())
        case.renderer.instance.calls.clear()
        case.renderer._bar_canvas.calls.clear()
        case.component.selected = 2
        self.assertTrue(case.draw())
        self.assertEqual(sum(x[0] == "write" for x in case.renderer.instance.calls), 3)
        self.assertEqual(case.renderer._bar_canvas.calls, [])
        self.assertGreater(case.renderer._perf_bar_skips, 0)

    def test_same_row_with_changed_fraction_only_repaints_bar_layer(self):
        case = self.make()
        fraction = [0.25]
        case.renderer._progress_fraction = lambda center, ref: fraction[0]
        self.assertTrue(case.draw())
        case.renderer.instance.calls.clear()
        case.renderer._bar_canvas.calls.clear()
        fraction[0] = 0.75
        self.assertTrue(case.draw())
        self.assertEqual(case.renderer.instance.calls, [])
        self.assertGreater(sum(x[0] == "fill" for x in case.renderer._bar_canvas.calls), 0)

    def test_no_bars_clears_stale_bar_layer_without_text_side_effects(self):
        case = self.make()
        self.assertTrue(case.draw())
        case.renderer.instance.calls.clear()
        case.renderer._bar_canvas.calls.clear()
        case.renderer._progress_fraction = lambda center, ref: None
        self.assertTrue(case.draw())
        self.assertTrue(any(x[0] == "clear" for x in case.renderer._bar_canvas.calls))
        self.assertEqual(case.renderer.instance.calls, [])

    def test_fallback_paints_everything_in_original_canvas(self):
        case = self.make(False)
        self.assertTrue(case.draw())
        self.assertEqual(sum(x[0] == "write" for x in case.renderer.instance.calls), 3)
        self.assertGreater(sum(x[0] == "fill" for x in case.renderer.instance.calls), 0)
        case.component.selected = 2
        case.renderer.instance.calls.clear()
        self.assertTrue(case.draw())
        self.assertGreater(sum(x[0] == "fill" for x in case.renderer.instance.calls), 0)


if __name__ == "__main__":
    unittest.main()
