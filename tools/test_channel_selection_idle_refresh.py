"""TEST7: unchanged ChannelSelection views skip heavy row reconstruction.

Run the *real* refresh method against a strict minimal Enigma2 fake. The
55ms timer and native font reassertion must run even on skipped draws.
Navigation, scrolling and refresh expiry must NEVER be delayed.
"""
import sys
from pathlib import Path
from time import monotonic
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_warder_channel_epg_clip import method, Canvas, Label


class IdleRefreshTests(unittest.TestCase):
    def make_case(self):
        draws, font_calls, timer_calls = [], [], []
        component = SimpleNamespace()
        native_view = SimpleNamespace(
            selected=3, top=0,
            size=lambda: SimpleNamespace(width=lambda: 1065, height=lambda: 842),
            getCurrentIndex=lambda: native_view.selected,
            getTopIndex=lambda: native_view.top,
            invalidate=lambda: None,
        )
        component.instance = native_view
        component.ServiceInfoFont = object()
        component.l = SimpleNamespace(
            celServiceInfo=3,
            setElementFont=lambda *args: font_calls.append(args))
        obj = SimpleNamespace(
            instance=Canvas(), _label=Label(),
            _component=component, _native_hidden=True,
            _native_disable_unsupported=False, _last=("valid-paint",),
            _idle_draw_key=(id(component), "barright", 0, 3, 1065, 842),
            _idle_draw_at=monotonic(),
            _scroll_mode="barright",
            _selected_title_scrollable=False,
            _timer=SimpleNamespace(start=lambda *args: timer_calls.append(args)),
            _diag=lambda *args: None,
            _find_component=lambda: component,
            _progress_mode=lambda: "barright",
            _draw_rows=lambda component: draws.append(component) or True,
            _restore_native=lambda: None,
        )
        return obj, native_view, draws, font_calls, timer_calls

    def run_refresh(self, obj):
        method("refresh")(obj)

    def test_idle_unchanged_screen_avoids_row_rebuild(self):
        obj, view, draws, fonts, timers = self.make_case()
        for _ in range(5):
            self.run_refresh(obj)
        self.assertEqual(draws, [])
        self.assertEqual(len(fonts), 5)
        self.assertEqual(len(timers), 5)
        self.assertTrue(all(t == (55, True) for t in timers))

    def test_navigation_selection_change_rebuilds_immediately(self):
        obj, view, draws, fonts, timers = self.make_case()
        view.selected = 4
        self.run_refresh(obj)
        self.assertEqual(len(draws), 1)

    def test_scrollable_selected_title_remains_full_speed(self):
        obj, view, draws, fonts, timers = self.make_case()
        obj._selected_title_scrollable = True
        self.run_refresh(obj)
        self.assertEqual(len(draws), 1)

    def test_expired_idle_check_rebuilds_data_and_bars(self):
        obj, view, draws, fonts, timers = self.make_case()
        obj._idle_draw_at = monotonic() - .26
        self.run_refresh(obj)
        self.assertEqual(len(draws), 1)

    def test_top_index_change_rebuilds_immediately(self):
        obj, view, draws, fonts, timers = self.make_case()
        view.top = 10
        self.run_refresh(obj)
        self.assertEqual(len(draws), 1)

    def test_explicit_source_change_forces_refresh(self):
        obj, view, draws, fonts, timers = self.make_case()
        obj._last = None
        self.run_refresh(obj)
        self.assertEqual(len(draws), 1)

    def test_geometry_change_forces_refresh(self):
        obj, view, draws, fonts, timers = self.make_case()
        view.size = lambda: SimpleNamespace(width=lambda: 900, height=lambda: 842)
        self.run_refresh(obj)
        self.assertEqual(len(draws), 1)


if __name__ == "__main__":
    unittest.main()
