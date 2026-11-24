"""Native API compatibility and passive overlay lifecycle regressions."""
from pathlib import Path
import importlib.util
import unittest
import ast
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "source/package-root/usr/lib/enigma2/python"
spec = importlib.util.spec_from_file_location("user_info_scroll", PAYLOAD / "Plugins/Extensions/setupGlass17/warderUserInfoScroll.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class Timer:
    def __init__(self):
        self.callback = []
        self.active = False
        self.delay = None
    def start(self, delay, single):
        assert single
        self.active = True
        self.delay = delay
    def stop(self):
        self.active = False


class NativeLabel:
    def __init__(self, modern=False):
        self.instance = object()
        self.pageHeight = 100
        self.modern = modern
        self.pos = 0
        self.calls = 0
        self.moves = []
        self.scroll_updates = 0
        self.showscrollbar = True
        self.scrollbar = object()
        self._height = "totalTextHeight" if modern else "TotalTextHeight"
        self._pos = "currentPosition" if modern else "curPos"
        setattr(self, self._height, 0)
        setattr(self, self._pos, 0)
    def setText(self, text):
        assert self.instance is not None
        self.calls += 1
        setattr(self, self._height, len(text) * 10)
        setattr(self, self._pos, 0)
        self.pos = 0
    def setPos(self, target):
        assert self.instance is not None
        self.pos = target
        setattr(self, self._pos, target)
        self.moves.append(target)
    def updateScrollbar(self):
        self.scroll_updates += 1
    def pageDown(self):
        raise AssertionError("Full-page jumps must not be used")


class Tests(unittest.TestCase):
    def test_short_static_and_long_independently_scroll(self):
        for modern in (False, True):
            a, b = NativeLabel(modern), NativeLabel(modern)
            ta, tb = Timer(), Timer()
            sa, sb = mod.DescriptionScroller(a, ta), mod.DescriptionScroller(b, tb)
            sa.set("short")
            sb.set("x" * 30)
            self.assertEqual((a.calls, b.calls), (0, 0))
            sa.show()
            sb.show()
            self.assertFalse(ta.active)
            self.assertTrue(tb.active)
            self.assertEqual(tb.delay, mod.START_DELAY)
            sb.tick()
            self.assertEqual(b.pos, 2)
            self.assertEqual(tb.delay, 55)
            sb.tick()
            self.assertEqual(b.pos, 4)
            self.assertEqual(a.pos, 0)
            self.assertEqual(b.scroll_updates, 0 if modern else 2)

    def test_clamped_endpoints_reverse_without_jumping(self):
        a, t = NativeLabel(), Timer()
        s = mod.DescriptionScroller(a, t)
        s.set("x" * 11)
        s.show()
        for _ in range(5):
            s.tick()
        self.assertEqual(a.moves, [2, 4, 6, 8, 10])
        self.assertEqual(t.delay, mod.END_DELAY)
        for _ in range(5):
            s.tick()
        self.assertEqual(a.moves[-5:], [8, 6, 4, 2, 0])
        self.assertEqual(t.delay, mod.START_DELAY)
        self.assertEqual(a.calls, 1)

    def test_refresh_keeps_position_until_event_changes(self):
        a, t = NativeLabel(), Timer()
        s = mod.DescriptionScroller(a, t)
        s.set("x" * 30, "event1")
        s.show()
        s.tick()
        calls = a.calls
        s.set("x" * 30, "event1")
        self.assertEqual(a.calls, calls)
        self.assertEqual(a.pos, 2)
        s.set("x" * 30, "event2")
        self.assertEqual(a.pos, 0)
        self.assertTrue(t.active)
        self.assertEqual(t.delay, mod.START_DELAY)

    def test_hide_close_and_no_widget(self):
        a, t = NativeLabel(), Timer()
        s = mod.DescriptionScroller(a, t)
        s.set("x" * 30)
        self.assertFalse(t.active)
        s.show()
        s.hide()
        s.tick()
        self.assertFalse(t.active)
        self.assertEqual(a.pos, 0)
        a.instance = None
        calls = a.calls
        s.set("new event")
        s.show()
        self.assertFalse(t.active)
        self.assertEqual(a.calls, calls)
        s.close()
        s.close()
        s.tick()
        s.show()
        s.set("ignored")
        self.assertEqual(t.callback, [])
        self.assertIsNone(s.label)
        self.assertIsNone(s.timer)

    def test_unknown_api_and_native_move_error_stop_safely(self):
        a, t = NativeLabel(), Timer()
        s = mod.DescriptionScroller(a, t)
        s.set("x" * 30)
        a.setPos = None
        s.show()
        self.assertFalse(t.active)
        def destroyed(_target):
            raise RuntimeError("native widget removed")
        a.setPos = destroyed
        s.show()
        self.assertTrue(t.active)
        s.tick()
        self.assertFalse(t.active)

    def test_all_seven_description_widgets_and_lifecycle(self):
        source = (PAYLOAD / "Screens/G17_UserInfo.py").read_text()
        ast.parse(source)
        import re
        widgets = re.findall(r'<widget name="description2?"[^>]*?/>', source)
        self.assertEqual(len(widgets), 7)
        for raw in widgets:
            node = ET.fromstring(raw)
            self.assertEqual(node.get("scrollbarMode"), "showOnDemand")
        self.assertEqual(source.count('self._initDescription("description")'), 4)
        self.assertEqual(source.count('self._initDescription("description2")'), 2)
        self.assertEqual(source.count('self._setDescription("description'), 4)
        for hook in ("onShow.append(self._showDescriptions)", "onHide.append(self._hideDescriptions)", "onClose.append(self._closeDescriptions)"):
            self.assertIn(hook, source)

if __name__ == "__main__":
    unittest.main()
