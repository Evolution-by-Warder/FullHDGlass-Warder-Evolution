"""Regression for FastScan and edited bouquet names in the EPG marquee.

Source-level geometry checks run without a receiver. They specifically detect
the case where the service-centre name or a hidden helper label is shorter
than the name actually painted by OpenATV's native ServiceList.
"""
import sys
import types
from unittest import TestCase
from unittest.mock import patch

from test_warder_channel_epg_clip import ClippedEventTests, method


def native_text_size(font, text, target_size, nowrap):
    # 17px/glyph simulates native eTextPara; the old hidden eLabel mock
    # deliberately returns only 10px/glyph.
    return types.SimpleNamespace(width=lambda: len(text) * 17)


class FastScanNameGeometryTests(TestCase):
    def case(self):
        case = ClippedEventTests(methodName="test_titles_never_reach_reserved_progress_column")
        case.setUp()
        case.service_stub.eLabel = types.SimpleNamespace(calculateTextSize=native_text_size)
        case.service_stub.eSize = lambda w, h: (w, h)
        return case

    def draw(self, case, column=None):
        func = method("_draw_rows")
        if column is not None:
            func.__globals__["config"].usage.servicelist_column = types.SimpleNamespace(value=str(column))
        with patch.dict(sys.modules, {"enigma": case.service_stub}):
            self.assertTrue(func(case.renderer, case.component))
        return [call for call in case.renderer.instance.calls if call[0] == "write"]

    def test_fastscan_bouquet_display_name_may_exceed_lamedb_name(self):
        case = self.case()
        case.refs[0].name = "FILMBOX"  # service-centre/lamedb name
        case.refs[0].getName = lambda: "FILMBOX+ Hits"  # bouquet display name
        writes = self.draw(case)
        first = next(call for call in writes if call[1][1] == 0)
        x, y, w, h = first[1]
        picon = int((37 + 2 * (-2)) * 167 / 100)
        boundary = 5 + picon + 2 * 8 + len("FILMBOX+ Hits") * 17
        self.assertGreaterEqual(x, boundary + 12)
        self.assertLessEqual(x + w, 700 - 25 - 90 - 12)

    def test_native_glyph_width_wins_over_underestimating_label(self):
        case = self.case()
        case.refs[0].name = "JOJ Cinema HD"
        writes = self.draw(case)
        first = next(call for call in writes if call[1][1] == 0)
        x = first[1][0]
        self.assertGreaterEqual(x, 5 + 55 + 16 + len("JOJ Cinema HD") * 17 + 12)

    def test_explicit_native_column_is_not_covered_by_epg(self):
        case = self.case()
        case.refs[0].name = "AXN CZ"
        writes = self.draw(case, column=350)
        first = next(call for call in writes if call[1][1] == 0)
        self.assertGreaterEqual(first[1][0], 5 + 55 + 16 + 350 + 12)

    def test_long_name_without_room_does_not_paint_over_native_name(self):
        case = self.case()
        case.refs[0].name = "Viasat Epic Drama HD and a deliberately very long suffix"
        writes = self.draw(case)
        self.assertFalse(any(call[1][1] == 0 for call in writes))
        self.assertTrue(any(call[1][1] == 37 for call in writes))

    def test_old_unnamed_bouquet_still_draws_and_scrolls(self):
        case = self.case()
        writes = self.draw(case)
        self.assertEqual(len(writes), 3)
        self.assertTrue(all(call[1][0] >= 0 and call[1][2] > 0 for call in writes))


if __name__ == "__main__":
    import unittest
    unittest.main()
