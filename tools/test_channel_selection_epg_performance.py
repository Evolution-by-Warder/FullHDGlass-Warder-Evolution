"""Behavioral regression for ChannelSelection event-progress query reuse.

Executes the real _draw_rows method with the established synthetic Enigma2
component/canvas test harness. These are call-count tests, not receiver FPS.
"""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_warder_channel_epg_clip import ClippedEventTests


class EpgProgressHotPathTests(unittest.TestCase):
    def make_case(self):
        case = ClippedEventTests(methodName="test_titles_never_reach_reserved_progress_column")
        case.setUp()
        return case

    def count_progress(self, case):
        called = []
        def get_progress(center, ref):
            called.append(ref)
            return 0.35
        case.renderer._progress_fraction = get_progress
        return called

    def test_native_bar_reuses_progress_for_text_and_bar(self):
        case = self.make_case()
        called = self.count_progress(case)
        self.assertTrue(case.draw())
        self.assertEqual(len(called), len(case.refs))
        self.assertEqual(len(set(map(id, called))), len(case.refs))
        self.assertTrue(any(x[0] == "fill" for x in case.renderer.instance.calls))
        self.assertEqual(sum(x[0] == "write" for x in case.renderer.instance.calls), 3)

    def test_empty_event_still_gets_progress_indicator(self):
        case = self.make_case()
        case.refs[1].title = ""
        called = self.count_progress(case)
        self.assertTrue(case.draw())
        self.assertEqual(len(called), len(case.refs))
        self.assertEqual(len(set(map(id, called))), len(case.refs))
        # Only title-bearing rows paint text; all rows retain their progressbar.
        self.assertEqual(sum(x[0] == "write" for x in case.renderer.instance.calls), 2)

    def test_non_bar_progress_modes_do_not_add_extra_queries(self):
        for mode in ("no", "percright", "minsleft"):
            with self.subTest(mode=mode):
                case = self.make_case()
                case.renderer._progress_mode = lambda m=mode: m
                called = self.count_progress(case)
                self.assertTrue(case.draw())
                self.assertEqual(len(called), len(case.refs))
                self.assertEqual(sum(x[0] == "write" for x in case.renderer.instance.calls), 3)

    def test_selection_change_keeps_one_progress_lookup_per_row(self):
        case = self.make_case()
        called = self.count_progress(case)
        self.assertTrue(case.draw())
        self.assertEqual(len(called), 3)
        called.clear()
        case.component.selected = 2
        self.assertTrue(case.draw())
        self.assertEqual(len(called), 3)


if __name__ == "__main__":
    unittest.main()
