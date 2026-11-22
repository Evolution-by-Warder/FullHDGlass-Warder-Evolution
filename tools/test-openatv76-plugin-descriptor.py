#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exercise the real plugin entry-point against old and new Descriptor APIs.

OpenATV 7.6 and OpenPLi 9.2 can expose WHERE_CHANNEL_CONTEXT_MENU without accepting the
serviceFilter constructor keyword. The optional country action must not
prevent FullHDGlass itself from loading.
"""
import ast
import os
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"


class LegacyDescriptor:
    WHERE_PLUGINMENU = 1
    WHERE_MENU = 2
    WHERE_SESSIONSTART = 3
    WHERE_CHANNEL_CONTEXT_MENU = 4
    WHERE_EXTENSIONSMENU = 5
    WHERE_EVENTINFO = 6

    def __init__(self, **kwargs):
        if "serviceFilter" in kwargs:
            raise TypeError("PluginDescriptor.__init__() got an unexpected keyword argument 'serviceFilter'")
        self.options = kwargs


class ModernDescriptor(LegacyDescriptor):
    def __init__(self, **kwargs):
        self.options = kwargs


class TestDescriptorCompatibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tree = ast.parse(PLUGIN.read_text(encoding="utf-8"), filename=str(PLUGIN))
        entry = next(node for node in tree.body
                     if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                     and node.name == "Plugins")
        cls.entry_code = compile(ast.Module(body=[entry], type_ignores=[]),
                                 str(PLUGIN), "exec")
        rds_guard = next(node for node in tree.body
                         if isinstance(node, ast.FunctionDef)
                         and node.name == "_warderGuardNativeRadioWindow")
        cls.rds_guard_code = compile(
            ast.Module(body=[rds_guard], type_ignores=[]), str(PLUGIN), "exec")

    def _run(self, descriptor):
        name = "warder_descriptor_compat_fixture"
        package = ModuleType(name)
        package.__path__ = []
        country = ModuleType(name + ".warderRadioCountry")
        country.open_country_selector = lambda *args, **kwargs: None
        country.is_live_service = lambda *args, **kwargs: True
        package.warderRadioCountry = country
        sys.modules[name] = package
        sys.modules[country.__name__] = country
        try:
            ns = {
                "__package__": name,
                "PluginDescriptor": descriptor,
                "config": SimpleNamespace(
                    skin=SimpleNamespace(primary_skin=SimpleNamespace(value="hd_glass17/skin.xml")),
                    plugins=SimpleNamespace(setupGlass17=SimpleNamespace(
                        par78=SimpleNamespace(value="n", getText=lambda: "Settings")))),
                "ui_text": lambda value: value,
                "main": lambda *args, **kwargs: None,
                "startSetup17": lambda *args, **kwargs: None,
                "startHdg17": lambda *args, **kwargs: None,
                "main17": lambda *args, **kwargs: None,
                "_warderOpenPliEpgReady": False,
            }
            exec(self.entry_code, ns)
            return ns["Plugins"](None)
        finally:
            sys.modules.pop(country.__name__, None)
            sys.modules.pop(name, None)

    def test_actual_upstream_descriptor_signature_when_provided(self):
        filename = os.environ.get("WARDER_UPSTREAM_PLUGIN", "")
        if not filename:
            self.skipTest("upstream Plugin.py not provided")
        tree = ast.parse(Path(filename).read_text(encoding="utf-8"), filename=filename)
        native = next(node for node in tree.body
                      if isinstance(node, ast.ClassDef)
                      and node.name == "PluginDescriptor")
        constructor = next(node for node in native.body
                           if isinstance(node, ast.FunctionDef)
                           and node.name == "__init__")
        # This is the real 7.6 / 9.2 constructor API, not only our fake:
        # both expose WHERE_CHANNEL_CONTEXT_MENU without serviceFilter.
        arguments = [arg.arg for arg in (constructor.args.posonlyargs +
                     constructor.args.args + constructor.args.kwonlyargs)]
        self.assertNotIn("serviceFilter", arguments)
        self.assertIsNone(constructor.args.kwarg)
        self.assertTrue(any(
            isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and
                target.id == "WHERE_CHANNEL_CONTEXT_MENU"
                for target in node.targets)
            for node in native.body), "Native context menu must be present")


    def test_openpli92_legacy_descriptor_still_loads_main_plugin(self):
        descriptors = self._run(LegacyDescriptor)
        self.assertEqual(len(descriptors), 3)
        self.assertFalse(any(
            "serviceFilter" in d.options for d in descriptors))


    def test_openatv76_legacy_descriptor_still_loads_main_plugin(self):
        descriptors = self._run(LegacyDescriptor)
        self.assertEqual(len(descriptors), 3)
        self.assertTrue(any(
            item.options.get("where") == LegacyDescriptor.WHERE_PLUGINMENU
            for item in descriptors))

    def test_newer_descriptor_keeps_optional_country_menu(self):
        descriptors = self._run(ModernDescriptor)
        self.assertEqual(len(descriptors), 4)
        self.assertTrue(any("serviceFilter" in item.options for item in descriptors))

    def test_rds_window_is_hidden_if_native_image_reopens_it_on_tv(self):
        class FakeRadioDisplay:
            def __init__(self):
                self.onShow = []
                self.hide_count = 0

            def hide(self):
                self.hide_count += 1

            def show(self):
                for callback in list(self.onShow):
                    callback()

        playing = {"ref": "tv"}
        nav = SimpleNamespace(getCurrentlyPlayingServiceReference=lambda: playing["ref"])
        bar = SimpleNamespace(session=SimpleNamespace(nav=nav))
        display = FakeRadioDisplay()
        ns = {"is_radio_reference": lambda ref: ref == "radio"}
        exec(self.rds_guard_code, ns)
        install = ns["_warderGuardNativeRadioWindow"]
        install(bar, display)
        install(bar, display)  # no duplicate callbacks across service changes
        self.assertEqual(len(display.onShow), 1)
        display.show()
        self.assertEqual(display.hide_count, 1)
        playing["ref"] = "radio"
        display.show()
        self.assertEqual(display.hide_count, 1)
        self.assertIn(
            "_warderGuardNativeRadioWindow(self, rds)",
            PLUGIN.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
