"""TEST6: exact progressbar paint equivalence and cache lifecycle.

The expected paint plan reproduces the approved TEST5 eight-segment algorithm
independently. Call traces must be PIXEL-IDENTICAL, not merely similar.
"""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_warder_channel_epg_clip import ClippedEventTests


def original_bar_calls(bx, by, bw, bh, fraction):
    border = "#dfdfdf"
    expected = [
        ("fill", (bx, by, bw, 2), border),
        ("fill", (bx, by + bh - 2, bw, 2), border),
        ("fill", (bx, by + 2, 2, bh - 4), border),
        ("fill", (bx + bw - 2, by + 2, 2, bh - 4), border),
    ]
    inner_width = bw - 4
    filled = int(inner_width * fraction)
    for segment in range(8):
        a = filled * segment // 8
        z = filled * (segment + 1) // 8
        if z <= a:
            continue
        t = ((a + z) / 2.0) / max(1, inner_width)
        if t < .55:
            u = t / .55
            rgb = (int(53 + 179 * u), int(177 + 23 * u), int(63 - 14 * u))
        else:
            u = (t - .55) / .45
            rgb = (232, int(200 - 139 * u), int(49 + 5 * u))
        expected.append(("fill", (bx + 2 + a, by + 2, z - a, bh - 4),
                         "#%02x%02x%02x" % rgb))
    return expected


class ProgressPaintCacheTests(unittest.TestCase):
    def case(self):
        case = ClippedEventTests(methodName="test_titles_never_reach_reserved_progress_column")
        case.setUp()
        case.renderer._progress_paint_cache = {}
        case.renderer._perf_bar_plan_hits = 0
        case.renderer._perf_bar_plan_misses = 0
        return case

    def test_original_colors_and_every_rectangle_match_for_all_fractions(self):
        for fraction in (0.0, .01, .05, .1, .25, .33, .5, .75, .95, .99, 1.0):
            with self.subTest(fraction=fraction):
                case = self.case()
                case.renderer._progress_fraction = lambda center, ref, value=fraction: value
                self.assertTrue(case.draw())
                paints = [call for call in case.renderer.instance.calls if call[0] == "fill"]
                # Fixture: width=700, right margin=25, bar width=90,
                # row height=37 and progressbar height=10.
                expected = []
                for row in range(3):
                    expected += original_bar_calls(585, row * 37 + 13, 90, 10, fraction)
                self.assertEqual(paints, expected)

    def test_repeated_selection_change_reuses_exact_paint_plan(self):
        case = self.case()
        self.assertTrue(case.draw())
        self.assertEqual(case.renderer._perf_bar_plan_misses, 1)
        self.assertEqual(case.renderer._perf_bar_plan_hits, 2)
        initial = [call for call in case.renderer.instance.calls if call[0] == "fill"]
        case.component.selected = 2
        case.renderer.instance.calls.clear()
        self.assertTrue(case.draw())
        self.assertEqual([call for call in case.renderer.instance.calls if call[0] == "fill"], initial)
        self.assertEqual(case.renderer._perf_bar_plan_misses, 1)
        self.assertEqual(case.renderer._perf_bar_plan_hits, 5)

    def test_changed_progress_fraction_rebuilds_plan_not_other_rows(self):
        case = self.case()
        fractions = {id(ref): .35 for ref in case.refs}
        case.renderer._progress_fraction = lambda center, ref: fractions[id(ref)]
        self.assertTrue(case.draw())
        self.assertEqual(len(case.renderer._progress_paint_cache), 1)
        fractions[id(case.refs[0])] = .85
        case.renderer.instance.calls.clear()
        self.assertTrue(case.draw())
        expected = []
        for row, ref in enumerate(case.refs):
            expected += original_bar_calls(585, row * 37 + 13, 90, 10, fractions[id(ref)])
        self.assertEqual([call for call in case.renderer.instance.calls if call[0] == "fill"], expected)
        self.assertEqual(len(case.renderer._progress_paint_cache), 2)

    def test_non_bar_mode_does_not_create_paint_plans(self):
        case = self.case()
        case.renderer._progress_mode = lambda: "no"
        self.assertTrue(case.draw())
        self.assertEqual(len(case.renderer._progress_paint_cache), 0)
        self.assertFalse(any(c[0] == "fill" for c in case.renderer.instance.calls))

    def test_plan_cache_stays_bounded_with_many_progress_variants(self):
        case = self.case()
        for pct in range(101):
            case.renderer._progress_fraction = lambda center, ref, value=pct/100.0: value
            case.renderer.instance.calls.clear()
            self.assertTrue(case.draw())
        self.assertLessEqual(len(case.renderer._progress_paint_cache), 128)


if __name__ == "__main__":
    unittest.main()
