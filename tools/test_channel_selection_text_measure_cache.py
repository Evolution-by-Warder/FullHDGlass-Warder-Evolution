"""TEST5 regressions for cached ChannelSelection row measurements.

Tests the actual _draw_rows method against the established mock canvas.
No real Enigma2 frame-time claims are made by these synthetic tests.
"""
from pathlib import Path
import sys
import unittest
from time import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_warder_channel_epg_clip import ClippedEventTests


class CountingLabel:
    def __init__(self):
        self.calls = 0
        self.text = ""

    def setFont(self, font):
        self.font = font

    def setText(self, text):
        self.text = text

    def calculateSize(self):
        self.calls += 1
        return type("Size", (), {"width": lambda _self: len(self.text) * 10})()


class RowMeasurementTests(unittest.TestCase):
    def setup_case(self):
        case = ClippedEventTests(methodName="test_titles_never_reach_reserved_progress_column")
        case.setUp()
        label = CountingLabel()
        case.renderer._label = label
        case.renderer._row_fit_cache = {}
        case.renderer._glyph_width_cache = {}
        case.renderer._perf_text_measure_calls = 0
        case.renderer._perf_text_cache_hits = 0
        return case, label

    def test_unchanged_rows_need_no_second_glyph_measurement(self):
        case, label = self.setup_case()
        self.assertTrue(case.draw())
        first_count = label.calls
        self.assertGreater(first_count, 3)
        case.renderer.instance.calls.clear()
        self.assertTrue(case.draw())
        self.assertEqual(label.calls, first_count)
        self.assertEqual(sum(x[0] == "write" for x in case.renderer.instance.calls), 0)
        self.assertGreater(case.renderer._perf_text_cache_hits, 0)

    def test_selection_movement_reuses_rows_and_preserves_highlight(self):
        case, label = self.setup_case()
        self.assertTrue(case.draw())
        count = label.calls
        case.component.selected = 2
        case.renderer.instance.calls.clear()
        self.assertTrue(case.draw())
        self.assertEqual(label.calls, count)
        writes = [c for c in case.renderer.instance.calls if c[0] == "write"]
        self.assertEqual(len(writes), 3)
        self.assertEqual(writes[2][2], "#62aaff")

    def test_changed_epg_title_invalidates_only_affected_row(self):
        case, label = self.setup_case()
        self.assertTrue(case.draw())
        count = label.calls
        case.refs[1].title = "New programme with different wording and duration" * 2
        case.renderer.instance.calls.clear()
        self.assertTrue(case.draw())
        self.assertGreater(label.calls, count)
        self.assertTrue(any("New programme" in call[-1] for call in case.renderer.instance.calls if call[0] == "write"))

    def test_scrolling_long_title_still_moves_inside_reserved_width(self):
        case, label = self.setup_case()
        case.component.selected = 0
        case.renderer._scroll_selected = 0
        case.renderer._scroll_started = time() - 8
        self.assertTrue(case.draw())
        initial = [c[-1] for c in case.renderer.instance.calls if c[0] == "write"][0]
        case.renderer._scroll_started = time() - 11
        case.renderer.instance.calls.clear()
        self.assertTrue(case.draw())
        updated = [c[-1] for c in case.renderer.instance.calls if c[0] == "write"][0]
        self.assertNotEqual(initial, updated)
        self.assertGreater(len(case.renderer._row_fit_cache), 0)


if __name__ == "__main__":
    unittest.main()
