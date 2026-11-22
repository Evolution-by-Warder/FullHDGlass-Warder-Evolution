#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guard Radio Live startup and radio-root MENU on legacy OpenATV/OpenPLi.

Run without a standalone WarderRadio extension; otherwise a passing test
could conceal the 7.6 / 9.2 boot regression.
"""
import ast
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
POSTINST = ROOT / "source/control/postinst"


def function(path, name):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == name)


def compile_functions(path, *names):
    nodes = [function(path, n) for n in names]
    return compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec")


class CountrySelection:
    def __init__(self, selected=True):
        current = ('FROM BOUQUET "userbouquet.warder.live.radio" ORDER BY bouquet'
                   if selected else 'FROM BOUQUET "userbouquet.private.radio" ORDER BY bouquet')
        self.current = SimpleNamespace(getPath=lambda: current)
        self.root = SimpleNamespace(
            getPath=lambda: 'FROM BOUQUET "bouquets.radio" ORDER BY bouquet')

    def getCurrentSelection(self):
        return self.current

    def getRoot(self):
        return self.root


class TestLegacyRadioLive(TestCase):
    def test_boot_controller_does_not_require_standalone_radio_plugin(self):
        events = []
        pkg = ModuleType("warder_legacy_test_pkg")
        pkg.__path__ = []
        extension = ModuleType("warder_legacy_test_pkg.warderRadioLive")
        extension.start = lambda reason, session=None: events.append((reason, session))
        with patch.dict(sys.modules, {
            pkg.__name__: pkg, extension.__name__: extension
        }):
            ns = {"__package__": pkg.__name__, "_controller": None}
            exec(compile_functions(PLUGIN_DIR / "warderRadioUpdate.py", "start"), ns)
            token = object()
            ns["start"](0, session=token)
            ns["start"](1, session=token)
        self.assertEqual(events, [(0, token), (1, token)])

    def test_installer_bootstraps_without_standalone_radio_plugin(self):
        source = POSTINST.read_text(encoding="utf-8")
        begin = source.index("# First-paint registration happens")
        end = source.index("# Download only the selected language", begin)
        block = source[begin:end]
        self.assertIn('"$warder_radio_country" --bootstrap', block)
        self.assertNotIn('warder_radio_browser', block)
        self.assertNotIn('WarderRadio/radio_browser.py', block)
        self.assertIn('Warder Radio Live', block)

    def _try_menu(self, openatv, selected=True):
        chosen = []

        class NativeMenu:
            def __init__(self, entries):
                self.list = entries

            def setList(self, entries):
                self.list = entries

        class OpenATVMenu(NativeMenu):
            def getList(self):
                return self.list

        class ChannelContextMenu(dict):
            def __init__(self, session, csel):
                super().__init__()
                self["menu"] = (OpenATVMenu if openatv else NativeMenu)(
                    [[("Nastavenia", lambda: None)]])
                self.closed = False

            def close(self, *args):
                self.closed = True

        def entry(key=None, text=None):
            return [text]

        screens = ModuleType("Screens")
        screens.__path__ = []
        native = ModuleType("Screens.ChannelSelection")
        native.ChannelContextMenu = ChannelContextMenu
        components = ModuleType("Components")
        components.__path__ = []
        choice = ModuleType("Components.ChoiceList")
        choice.ChoiceEntryComponent = entry
        parent = ModuleType("warder_legacy_test_pkg")
        parent.__path__ = []
        ui = ModuleType("warder_legacy_test_pkg.warderUiText")
        ui.ui_text = lambda x: x

        ns = {
            "__package__": parent.__name__,
            "live": SimpleNamespace(FILE="userbouquet.warder.live.radio"),
            "open_country_selector": lambda session, channel_selection=None:
                chosen.append(channel_selection),
        }
        with patch.dict(sys.modules, {
            "Screens": screens, "Screens.ChannelSelection": native,
            "Components": components, "Components.ChoiceList": choice,
            parent.__name__: parent, ui.__name__: ui,
        }):
            exec(compile_functions(PLUGIN_DIR / "warderRadioCountry.py",
                                   "_is_live_bouquet_selected",
                                   "install_root_country_menu"), ns)
            self.assertTrue(ns["install_root_country_menu"]())
            selected_bouquet = CountrySelection(selected)
            ctx = ChannelContextMenu(object(), selected_bouquet)
            entries = ctx["menu"].list
            if selected:
                self.assertEqual(len(entries), 2)
                self.assertIn("Select country", entries[1][0][0])
                callback = entries[1][0][1]
                callback()
                self.assertEqual(chosen, [selected_bouquet])
                self.assertTrue(ctx.closed)
            else:
                self.assertEqual(len(entries), 1)
                self.assertEqual(chosen, [])

    def test_openatv76_native_context_menu(self):
        self._try_menu(openatv=True)

    def test_openpli92_native_context_menu(self):
        self._try_menu(openatv=False)

    def test_other_radio_bouquets_unchanged(self):
        for openatv in (True, False):
            self._try_menu(openatv=openatv, selected=False)


if __name__ == "__main__":
    main()
