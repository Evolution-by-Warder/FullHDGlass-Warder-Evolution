"""Regression: a selection repaint must not reuse stale EPG x-coordinates.

Receiver reproduction: the same FastScan rows show overlapping names with
CANAL+ Drama selected, then correct EPG placement on moving to FILMBOX+ One.
This isolated test makes the text metric change across native repaint calls.
"""
import sys
import types
import unittest
from unittest.mock import patch

from test_warder_channel_epg_clip import ClippedEventTests, method


class VariableLabel:
    def __init__(self):
        self.multiplier = 10
        self.calls = 0
        self.text = ""

    def setFont(self, font):
        self.font = font

    def setText(self, text):
        self.text = text

    def calculateSize(self):
        self.calls += 1
        return types.SimpleNamespace(width=lambda: self.multiplier * len(self.text))


class FastScanSelectionRepaintTests(unittest.TestCase):
    def setUp(self):
        self.case = ClippedEventTests(methodName="test_titles_never_reach_reserved_progress_column")
        self.case.setUp()
        self.label = VariableLabel()
        self.case.renderer._label = self.label
        self.case.renderer._row_fit_cache = {}
        self.case.renderer._glyph_width_cache = {}

    def draw(self):
        with patch.dict(sys.modules, {"enigma": self.case.service_stub}):
            result = method("_draw_rows")(self.case.renderer, self.case.component)
        self.assertTrue(result)
        return [item for item in self.case.renderer.instance.calls if item[0] == "write"]

    def test_focus_change_refreshes_all_cached_row_coordinates(self):
        self.case.component.selected = 0
        first = self.draw()
        first_x = first[0][1][0]
        cached_first = dict(self.case.renderer._row_fit_cache)
        self.assertTrue(cached_first)
        self.label.multiplier = 16
        self.case.component.selected = 1
        self.case.renderer.instance.calls.clear()
        second = self.draw()
        self.assertGreater(second[0][1][0], first_x)
        self.assertGreater(self.label.calls, 0)

    def test_same_focus_retains_cache_on_stationary_frame(self):
        self.case.component.selected = 0
        self.draw()
        calls = self.label.calls
        self.case.renderer.instance.calls.clear()
        self.draw()
        self.assertEqual(self.label.calls, calls)

    def test_page_shift_refreshes_cached_name_measurements(self):
        self.case.component.selected = 2
        self.draw()
        self.label.multiplier = 16
        self.case.component.getTopIndex = lambda: 1
        self.case.renderer.instance.calls.clear()
        rows = self.draw()
        self.assertEqual(rows[0][1][1], 0)  # first visible row
        self.assertEqual(self.case.renderer._last_visible_top, 1)

    def test_existing_channel_fonts_and_scroll_settings_are_preserved(self):
        self.case.component.selected = 0
        self.draw()
        self.assertEqual(self.case.component.ServiceNameFont, "name")
        self.assertEqual(self.case.component.ServiceInfoFont, "info")


if __name__ == "__main__":
    unittest.main()
