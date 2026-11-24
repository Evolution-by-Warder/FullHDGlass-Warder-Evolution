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
    def start(self, delay, single):
        assert delay == 5000 and single
        self.active = True
    def stop(self):
        self.active = False

class NativeLabel:
    def __init__(self, modern=False):
        self.instance = object()
        self.pageHeight = 100
        self.modern = modern
        self.pos = 0
        self.calls = 0
        self.TotalTextHeight = 0
        if modern:
            self.isNavigationNeeded = lambda: self.TotalTextHeight > self.pageHeight
    def setText(self, text):
        self.calls += 1
        self.TotalTextHeight = len(text) * 10
        self.pos = 0
    def pageDown(self):
        self.pos = min(self.pos + self.pageHeight, self.TotalTextHeight - self.pageHeight)
    def isAtLastPage(self):
        return self.TotalTextHeight <= self.pageHeight or self.pos == self.TotalTextHeight - self.pageHeight

class Tests(unittest.TestCase):
    def test_short_static_and_long_independently_scroll(self):
        for modern in (False, True):
            a, b = NativeLabel(modern), NativeLabel(modern)
            ta, tb = Timer(), Timer()
            sa, sb = mod.DescriptionScroller(a, ta), mod.DescriptionScroller(b, tb)
            sa.set("short")
            sb.set("x" * 30)
            sa.show()
            sb.show()
            self.assertFalse(ta.active)
            self.assertTrue(tb.active)
            sb.tick()
            self.assertEqual(b.pos, 100)
            sb.tick()
            self.assertEqual(b.pos, 200)
            sb.tick()
            self.assertEqual(b.pos, 0)
            self.assertEqual(a.pos, 0)

    def test_refresh_keeps_position_until_event_changes(self):
        a, t = NativeLabel(), Timer()
        s = mod.DescriptionScroller(a, t)
        s.set("x" * 30, "event1")
        s.show()
        s.tick()
        calls = a.calls
        s.set("x" * 30, "event1")
        self.assertEqual(a.calls, calls)
        self.assertEqual(a.pos, 100)
        s.set("x" * 30, "event2")
        self.assertEqual(a.pos, 0)
        self.assertTrue(t.active)

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
        s.show()
        self.assertFalse(t.active)
        s.close()
        self.assertEqual(t.callback, [])

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
