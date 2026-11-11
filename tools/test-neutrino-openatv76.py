#!/usr/bin/env python3
"""Integration checks against the pinned upstream OpenATV 7.6 source.

This executes the *actual* 7.6 long-key detector and service-list method
together with Warder's short-OK handler in a minimal Enigma2-like harness.
It is not a substitute for testing a Vu+ Solo 4K remote control.
"""
import argparse
import ast
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
WARDER_MAP = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/keymap.xml"
UPSTREAM = None


def load_function(filename, function, cls=None):
    tree = ast.parse(Path(filename).read_text(encoding="utf-8"), filename=str(filename))
    body = tree.body
    if cls:
        matches = [n for n in body if isinstance(n, ast.ClassDef) and n.name == cls]
        assert len(matches) == 1, (cls, filename)
        body = matches[0].body
    matches = [n for n in body if isinstance(n, ast.FunctionDef) and n.name == function]
    assert len(matches) == 1, (function, filename)
    code = compile(ast.fix_missing_locations(ast.Module(body=[matches[0]], type_ignores=[])),
                   str(filename), "exec")
    return code


def key(context, name, filename):
    root = ET.parse(filename).getroot()
    maps = [m for m in root.findall("map") if m.get("context") == context]
    assert len(maps) == 1, (context, filename)
    return [n for n in maps[0].findall("key") if n.get("id") == name]


class OpenATV76NeutrinoTest(unittest.TestCase):
    def setUp(self):
        self.native = UPSTREAM / "lib/python/Screens/InfoBarGenerics.py"
        self.native_map = UPSTREAM / "data/keymap.ntr"
        self.parser = UPSTREAM / "lib/python/Components/ActionMap.py"
        for path in (self.native, self.native_map, self.parser, PLUGIN, WARDER_MAP):
            self.assertTrue(path.is_file(), str(path))

    def test_exact_native_76_keys_and_flags(self):
        native_ok = key("InfobarChannelSelection", "KEY_OK", self.native_map)
        self.assertTrue(any(n.get("mapto") == "openServiceList" and
                            "m" in n.get("flags", "") for n in native_ok))
        self.assertTrue(any(n.get("mapto") == "LongOKPressed" and
                            "l" in n.get("flags", "") for n in
                            key("InfobarShowHideActions", "KEY_OK", self.native_map)))
        for context in ("g17Actions_neutrino", "g17Actions_neutrinoSpecial"):
            self.assertEqual([(n.get("mapto"), n.get("flags"))
                              for n in key(context, "KEY_OK", WARDER_MAP)],
                             [("warder_neutrino_channel_list", "b")])
        for context in ("g17Actions", "g17ActionsSpecial"):
            self.assertEqual([(n.get("mapto"), n.get("flags"))
                              for n in key(context, "KEY_OK", WARDER_MAP)],
                             [("ok_pressed", "m")])
        source = self.parser.read_text(encoding="utf-8")
        for flag, mask in (("m", 1), ("b", 2), ("r", 4), ("l", 8)):
            self.assertRegex(source, r'["\\\']' + flag + r'["\\\']\\s*:\\s*' + str(mask))

    def test_upstream_76_short_and_long_native_dispatch(self):
        namespace = {}
        exec(load_function(self.native, "detection", "InfoBarLongKeyDetection"), namespace)
        detect = namespace["detection"]
        exec(load_function(self.native, "openServiceList", "InfoBarChannelSelection"), namespace)
        native_open = namespace["openServiceList"]

        config = SimpleNamespace(
            skin=SimpleNamespace(autorefresh=SimpleNamespace(value=False)),
            plugins=SimpleNamespace(setupGlass17=SimpleNamespace(
                par34=SimpleNamespace(value=True))))
        class Session:
            def __init__(self):
                self.current_dialog = None
                self.opens = 0
            def execDialog(self, dialog):
                self.opens += 1
                self.current_dialog = dialog
        class InfoBar:
            openServiceList = native_open
            def __init__(self):
                self.session = Session()
                self.servicelist = object()
                self.LongButtonPressed = False
        warder = {"InfoBar": InfoBar, "config": config}
        exec(load_function(PLUGIN, "warderNeutrinoChannelList17"), warder)
        handler = warder["warderNeutrinoChannelList17"]
        namespace["config"] = config  # native openServiceList resolves the same config

        def press(box, events, native_short_active):
            for flag in events:
                detect(box, 352, flag)  # KEY_OK Linux input code
                if flag == 0 and native_short_active:
                    box.openServiceList()  # OpenATV 7.6 KEY_OK 'm'
                if flag == 1:
                    handler(box)  # Warder KEY_OK 'b' release

        # If 7.6 handles KEY_OK at key-down, Warder must not open it twice.
        box = InfoBar()
        press(box, [0, 1], True)
        self.assertEqual(box.session.opens, 1)
        self.assertIs(box.session.current_dialog, box.servicelist)

        # If the original action gets swallowed, Warder can supply the missing short OK.
        box = InfoBar()
        press(box, [0, 1], False)
        self.assertEqual(box.session.opens, 1)

        # A long press must never be mistaken for a short release.
        box = InfoBar()
        press(box, [0, 3, 1], False)
        self.assertTrue(box.LongButtonPressed)
        self.assertEqual(box.session.opens, 0)

        # Existing long OK upstream handling is not intercepted or remapped.
        box = InfoBar()
        press(box, [0, 3, 1], True)
        self.assertEqual(box.session.opens, 1)

        # The additional handler is disabled with the Warder Neutrino setting.
        config.plugins.setupGlass17.par34.value = False
        box = InfoBar()
        press(box, [0, 1], False)
        self.assertEqual(box.session.opens, 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream", required=True, type=Path)
    parsed, remaining = parser.parse_known_args()
    UPSTREAM = parsed.upstream
    unittest.main(argv=[sys.argv[0]] + remaining)
