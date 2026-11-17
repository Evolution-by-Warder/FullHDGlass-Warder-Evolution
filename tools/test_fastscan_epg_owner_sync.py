"""Receiver-independent regressions for exact ChannelSelection EPG ownership.

A FastScan bouquet may be opened in a separate ChannelSelection while the
global InfoBar keeps a different list. The marquee must only use the list
owned by its own screen, never the global singleton.
"""
import types
import sys
import unittest
from unittest.mock import patch

from test_warder_channel_epg_clip import ClippedEventTests, method


class EpgOwnerSyncTests(unittest.TestCase):
    def setup_case(self):
        case = ClippedEventTests(methodName="test_titles_never_reach_reserved_progress_column")
        case.setUp()
        case.component.l.getList = case.component.getList
        return case

    def test_overlay_uses_its_own_screen_list_not_global_infobar_list(self):
        case = self.setup_case()
        different_global_component = types.SimpleNamespace(
            ServiceInfoFont="wrong-info", ServiceNameFont="wrong-name")
        fake_infobar = types.ModuleType("Screens.InfoBar")
        fake_infobar.InfoBar = types.SimpleNamespace(
            instance=types.SimpleNamespace(
                servicelist={"list": different_global_component}))
        target = types.SimpleNamespace(
            _warder_owner_screen={"list": case.component},
            _diag=lambda *args: None)
        with patch.dict(sys.modules, {"Screens.InfoBar": fake_infobar}):
            resolved = method("_find_component")(target)
        self.assertIs(resolved, case.component)
        self.assertIsNot(resolved, different_global_component)

    def test_unknown_owner_fails_closed_instead_of_global_fallback(self):
        case = self.setup_case()
        target = types.SimpleNamespace(_diag=lambda *args: None)
        self.assertIsNone(method("_find_component")(target))

    def test_bad_owner_list_fails_closed(self):
        target = types.SimpleNamespace(
            _warder_owner_screen={"list": object()},
            _diag=lambda *args: None)
        self.assertIsNone(method("_find_component")(target))

    def test_selected_service_mismatch_does_not_paint_wrong_event(self):
        case = self.setup_case()
        case.component.getCurrent = lambda: types.SimpleNamespace(
            toString=lambda: "a-different-bouquet-service")
        for ref in case.refs:
            ref.toString = lambda: "native-service"
        with patch.dict(sys.modules, {"enigma": case.service_stub}):
            result = method("_draw_rows")(case.renderer, case.component)
        self.assertFalse(result)
        self.assertFalse(any(item[0] == "write" for item in case.renderer.instance.calls))

    def test_actual_native_selected_service_still_paints(self):
        case = self.setup_case()
        for idx, ref in enumerate(case.refs):
            ref.toString = lambda idx=idx: "service-" + str(idx)
        case.component.getCurrent = lambda: case.refs[case.component.selected]
        with patch.dict(sys.modules, {"enigma": case.service_stub}):
            result = method("_draw_rows")(case.renderer, case.component)
        self.assertTrue(result)
        self.assertEqual(sum(c[0] == "write" for c in case.renderer.instance.calls), 3)


if __name__ == "__main__":
    unittest.main()
