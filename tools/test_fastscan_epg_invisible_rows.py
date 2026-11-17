"""Regression for real native eListboxServiceContent hidden FastScan rows.

OpenATV C++ getList() returns raw entries, but cursorResolve(), size() and
cursorMove() exclude flag isInvisible=512 and optionally isNumberedMarker=256.
Thus GUI getCurrentIndex()/getTopIndex() are VISIBLE indexes, not raw indexes.
"""
import sys
import types
import unittest
from unittest.mock import patch
from test_warder_channel_epg_clip import ClippedEventTests, Service, method


class FastScanInvisibleRowsTests(unittest.TestCase):
    def setup_case(self, hide_numbered=False, edit_mode=False):
        case = ClippedEventTests(methodName="test_titles_never_reach_reserved_progress_column")
        case.setUp()
        drama = Service("CANAL+ Drama", "Hotel na pobrezi")
        invisible = Service("Hidden separator", "must never paint")
        invisible.flags = 512
        one = Service("FILMBOX+ One", "Simon a Matous")
        love = Service("FILMBOX+ Love", "Vrazdy pro")
        for index, ref in enumerate((drama, invisible, one, love)):
            ref.flags = getattr(ref, "flags", 0)
            ref.toString = (lambda idx=index: "service-%d" % idx)
        case.refs = [drama, invisible, one, love]
        case.component.refs = case.refs
        case.component.selected = 1  # second native VISIBLE row = FILMBOX One
        case.component.getCurrent = lambda: one
        case.component.getMarked = lambda: ["moving"] if edit_mode else []
        mock_service = case.service_stub
        draw = method("_draw_rows")
        draw.__globals__["config"].usage.hide_number_markers = types.SimpleNamespace(value=hide_numbered)
        return case, draw, mock_service

    def draw(self, case, fn, service_stub):
        with patch.dict(sys.modules, {"enigma": service_stub}):
            ok = fn(case.renderer, case.component)
        return ok, [(x[1][1], x[-1]) for x in case.renderer.instance.calls if x[0] == "write"]

    def test_fastscan_invisible_entry_does_not_shift_epg_down_a_row(self):
        case, fn, stub = self.setup_case()
        ok, writes = self.draw(case, fn, stub)
        self.assertTrue(ok)
        self.assertEqual(writes, [(0, "Hotel na pobrezi"), (37, "Simon a Matous"), (74, "Vrazdy pro")])
        self.assertTrue(all("Hidden" not in text and "must never" not in text for _, text in writes))

    def test_native_selection_is_checked_against_visible_service_not_raw_offset(self):
        case, fn, stub = self.setup_case()
        case.component.getCurrent = lambda: case.refs[2]
        ok, writes = self.draw(case, fn, stub)
        self.assertTrue(ok)
        self.assertEqual(writes[1][1], "Simon a Matous")

    def test_hidden_numbered_markers_follow_native_hide_setting(self):
        case, fn, stub = self.setup_case(hide_numbered=True)
        numbered = Service("numbered marker", "not painted")
        numbered.flags = 256 | 64
        numbered.toString = lambda: "marker"
        case.refs.insert(1, numbered)
        ok, writes = self.draw(case, fn, stub)
        self.assertTrue(ok)
        self.assertEqual([text for _, text in writes], ["Hotel na pobrezi", "Simon a Matous", "Vrazdy pro"])

    def test_numbered_marker_in_edit_mode_retains_native_visible_row(self):
        case, fn, stub = self.setup_case(hide_numbered=True, edit_mode=True)
        marker = Service("Visible marker", "")
        marker.flags = 256 | 64
        marker.toString = lambda: "marker"
        case.refs.insert(1, marker)
        case.component.selected = 2
        ok, writes = self.draw(case, fn, stub)
        self.assertTrue(ok)
        self.assertEqual(writes, [(0, "Hotel na pobrezi"), (74, "Simon a Matous"), (111, "Vrazdy pro")])

    def test_page_top_index_is_interpreted_after_hidden_rows_removed(self):
        case, fn, stub = self.setup_case()
        case.component.getTopIndex = lambda: 1
        ok, writes = self.draw(case, fn, stub)
        self.assertTrue(ok)
        self.assertEqual(writes, [(0, "Simon a Matous"), (37, "Vrazdy pro")])

    def test_safe_native_fallback_when_marked_state_is_unknown(self):
        case, fn, stub = self.setup_case(hide_numbered=True)
        marker = Service("numbered marker", "none")
        marker.flags = 256 | 64
        case.refs.insert(1, marker)
        case.component.getMarked = None
        ok, writes = self.draw(case, fn, stub)
        self.assertFalse(ok)
        self.assertEqual(writes, [])


if __name__ == "__main__":
    unittest.main()
