#!/usr/bin/env python3
"""Regressions: IPTV service names must survive a missing bouquet number."""
import ast
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / "source/package-root/usr/lib/enigma2/python"
MODULE = PYTHON / "Components/Converter/g17ServiceNum.py"
LAYOUT = PYTHON / "Screens/G17screens.py"


class FakePlayable:
    def __init__(self, name):
        self._info = SimpleNamespace(getName=lambda *args: name)
    def info(self):
        return self._info


class FakeReference:
    def __init__(self, name):
        self.name = name
    def getName(self):
        return self.name


class BaseConverter:
    def __init__(self, kind):
        self.kind = kind


class Center:
    @staticmethod
    def getInstance():
        return Center()


def load_converter():
    config = SimpleNamespace(plugins=SimpleNamespace(setupGlass17=SimpleNamespace(
        par126=SimpleNamespace(value="1"),
        par79=SimpleNamespace(value="1"),
    )))
    modules = {}
    for name in ("Components", "Components.config", "Components.Converter",
                 "Components.Converter.Converter", "Components.Element", "enigma",
                 "Plugins", "Plugins.Extensions", "Plugins.Extensions.setupGlass17",
                 "Plugins.Extensions.setupGlass17.weaUtils",
                 "Plugins.Extensions.setupGlass17.py38"):
        modules[name] = ModuleType(name)
    modules["Components.config"].config = config
    modules["Components.Converter.Converter"].Converter = BaseConverter
    modules["Components.Element"].cached = lambda fn: fn
    modules["enigma"].eServiceCenter = Center
    modules["enigma"].eServiceReference = FakeReference
    modules["enigma"].iServiceInformation = SimpleNamespace(sServiceref=0)
    modules["enigma"].iPlayableServicePtr = FakePlayable
    modules["enigma"].eDVBFrontendParametersTerrestrial = SimpleNamespace(
        System_DVB_T=1, System_DVB_T2=2)
    modules["Plugins.Extensions.setupGlass17.weaUtils"].ISP38 = True
    modules["Plugins.Extensions.setupGlass17.py38"].DG = "°"
    with patch.dict(sys.modules, modules):
        spec = importlib.util.spec_from_file_location("isolated_g17ServiceNum", MODULE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module.g17ServiceNum


def converter(channel_name, reference_name="", number="", platform=""):
    obj = load_converter()("NumberAndName")
    obj.source = SimpleNamespace(
        service=FakePlayable(channel_name),
        serviceref=FakeReference(reference_name),
    )
    obj.isEnaNumber = lambda: number
    obj.isEnaSat = lambda ref, info: platform
    return obj


def fail(*args):
    raise RuntimeError("IPTV bouquet has no valid channel number")


class IPTVNameTests(unittest.TestCase):
    def test_iptv_name_is_not_lost_if_number_lookup_fails(self):
        obj = converter("IPTV: BBC World")
        obj.isEnaNumber = fail
        self.assertEqual(obj.text, "IPTV: BBC World")

    def test_iptv_playlist_name_fallback_if_decoder_has_no_name(self):
        obj = converter("", "IPTV Playlist Name")
        obj.isEnaNumber = fail
        self.assertEqual(obj.text, "IPTV Playlist Name")

    def test_bad_number_and_platform_lookup_cannot_hide_name(self):
        obj = converter("IPTV: Eurosport")
        obj.isEnaNumber = fail
        obj.isEnaSat = fail
        self.assertEqual(obj.text, "IPTV: Eurosport")

    def test_normal_dvb_number_and_satellite_prefix_unchanged(self):
        self.assertEqual(converter("DVB Channel", number="41. ", platform="(DVB-T2) ").text,
                         "41. (DVB-T2) DVB Channel")

    def test_missing_names_are_visible_instead_of_blank_or_exception(self):
        obj = converter("")
        obj.isEnaNumber = fail
        self.assertEqual(obj.text, "Unknown Channel")

    def test_infobar_1_and_76_have_different_service_name_converters(self):
        tree = ast.parse(LAYOUT.read_text(encoding="utf-8"))
        screens = {}
        for node in tree.body:
            if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Subscript)
                and isinstance(node.targets[0].value, ast.Name)
                and node.targets[0].value.id == "g17_extraScreen"
                and isinstance(node.targets[0].slice, ast.Constant)
                and node.targets[0].slice.value in ("1", "76")
                and isinstance(node.value, ast.Constant)):
                screens[node.targets[0].slice.value] = ET.fromstring(node.value.value)
        self.assertEqual(set(screens), {"1", "76"})
        def types(screen):
            return [elem.attrib.get("type") for elem in screen.iter("convert")]
        self.assertIn("ServiceName", types(screens["1"]))
        self.assertIn("g17ServiceNum", types(screens["76"]))


if __name__ == "__main__":
    unittest.main()
