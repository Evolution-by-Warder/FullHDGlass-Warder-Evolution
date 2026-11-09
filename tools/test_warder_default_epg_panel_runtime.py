"""Simulate the default ChannelSelection runtime geometry patch without Enigma2.

Receiver QA identified a real 10px intersection between description and
upcoming EPG. Only a generated runtime skin may be adjusted; never the
approved source skin.xml or user font sizes.
"""
import ast
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
BASE = ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml"


class DefaultEpgPanelRuntimeTests(unittest.TestCase):
    def test_scroll_is_opt_in_and_uses_complete_line_heights(self):
        renderer = (ROOT / "source/package-root/usr/lib/enigma2/python/Components/Renderer/g17MetrixHDRunningText.py").read_text(encoding="utf-8")
        self.assertIn('self.warderWholeLineScroll = False', renderer)
        self.assertIn('elif attrib == "warderWholeLineScroll":', renderer)
        self.assertIn('self.H = (self.H // self.lineHeight) * self.lineHeight', renderer)
        self.assertIn('self.lineHeight = flh', renderer)
        self.assertIn('or self.warderWholeLineScroll:', renderer)
        self.assertIn('self.mStep = 2', renderer)
        self.assertIn('self.mStepTimeout = 55', renderer)
        self.assertNotIn('self.mStepTimeout = max(self.mStepTimeout, 800)', renderer)
        # The layout hook is limited to the default ChannelSelection screen.
        source = PLUGIN.read_text(encoding="utf-8")
        self.assertIn('if in_default_channel_screen and', source)
        self.assertIn('warderWholeLineScroll="1"', source)

    def test_custom_font_pass_does_not_drop_last_service_event_overlay(self):
        # Receiver TEST61 proved the installed skin had lost the overlay.
        # A terminal self-closing ServiceEvent widget was buffered in
        # changeChF() and discarded at </screen>. Exercise both actual
        # plugin functions in their native sequence with enlarged fonts.
        original = BASE.read_text(encoding="utf-8")
        tree = ast.parse(PLUGIN.read_text(encoding="utf-8"))
        names = {"cChannelsel", "changeChF"}
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
                 and n.name in names]
        self.assertEqual({n.name for n in nodes}, names)

        def setting(value):
            return SimpleNamespace(value=value)

        plugin_config = SimpleNamespace(
            par109=setting("#cdcdcd"), par110=setting("#6cbcf0"),
            par111=setting("#6cbcf0"), par117=setting("#dddddd"),
            par145=setting("40"), par146=setting("38"),
            par147=setting("1"), par148=setting("30"))
        with TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "skin.xml"
            runtime.write_text(original, encoding="utf-8")

            def write_text(path, text):
                self.assertEqual(Path(path), runtime)
                runtime.write_text(text, encoding="utf-8")
                return True

            def calc(line, key, new):
                import re
                return re.sub(re.escape(key) + r'[^"]*',
                              lambda m: key + str(new), line, count=1)

            scope = dict(config=SimpleNamespace(plugins=SimpleNamespace(
                setupGlass17=plugin_config,
                warderEpgListScroll=SimpleNamespace(enabled=setting(True)))), SKINXML=str(runtime),
                ENA_P_CH=False, _atomicWriteText=write_text, calc=calc, re=re, allow_channel_epg_overlay=lambda: True, allow_channel_epg_overlay=lambda: True)
            exec(compile(ast.Module(body=nodes, type_ignores=[]),
                         str(PLUGIN), "exec"), scope)
            self.assertEqual(scope["cChannelsel"](), "c")
            self.assertEqual(scope["changeChF"](), "o")
            result = runtime.read_text(encoding="utf-8")
            screen = result.split('<screen name="ChannelSelection"', 1)[1].split('</screen>', 1)[0]
            self.assertEqual(screen.count('render="WarderChannelEpgClip"'), 1)
            self.assertIn('numEvents="6"', screen)
            self.assertIn('serviceNameFont="Prive4;40"', screen)
            self.assertIn('serviceInfoFont="Prive4;38"', screen)
            self.assertNotIn('warderTestMarker=', screen)
            # Repeated font application should also be idempotent.
            self.assertEqual(scope["changeChF"](), "o")
            screen2 = runtime.read_text(encoding="utf-8").split(
                '<screen name="ChannelSelection"', 1)[1].split('</screen>', 1)[0]
            self.assertEqual(screen2.count('render="WarderChannelEpgClip"'), 1)
            self.assertEqual(BASE.read_text(encoding="utf-8"), original)

    def test_native_default_removes_persisted_overlay(self):
        original = BASE.read_text(encoding="utf-8")
        overlay = ('    <widget source="ServiceEvent" render="WarderChannelEpgClip" '
                   'position="60,96" size="1065,842" zPosition="4" '
                   'warderProgressWidth="90" alphaTest="blend" transparent="1" />\\n')
        end = original.index("</screen>", original.index('<screen name="ChannelSelection"'))
        original = original[:end] + overlay + original[end:]
        tree = ast.parse(PLUGIN.read_text(encoding="utf-8"))
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "cChannelsel")
        def setting(value):
            return SimpleNamespace(value=value)
        conf = SimpleNamespace(
            setupGlass17=SimpleNamespace(
                par109=setting("#cdcdcd"), par110=setting("#6cbcf0"),
                par111=setting("#6cbcf0"), par117=setting("#dddddd")),
            warderEpgListScroll=SimpleNamespace(enabled=setting(False)))
        with TemporaryDirectory() as td:
            runtime = Path(td) / "skin.xml"
            runtime.write_text(original, encoding="utf-8")
            scope = dict(config=SimpleNamespace(plugins=conf), SKINXML=str(runtime),
                         ENA_P_CH=False, isOpenPLi=False, re=re, allow_channel_epg_overlay=lambda: True,
                         _atomicWriteText=lambda p, content: Path(p).write_text(content, encoding="utf-8"))
            exec(compile(ast.Module(body=[fn], type_ignores=[]), str(PLUGIN), "exec"), scope)
            self.assertEqual(scope["cChannelsel"](), "c")
            result = runtime.read_text(encoding="utf-8")
            screen = result.split('<screen name="ChannelSelection"', 1)[1].split('</screen>', 1)[0]
            self.assertNotIn('render="WarderChannelEpgClip"', screen)
            self.assertIn('picServiceEventProgressbar=', screen)
            self.assertIn('render="WarderPrimeTime"', screen)
            self.assertEqual(scope["cChannelsel"](), "c")
            self.assertEqual(runtime.read_text(encoding="utf-8"), result)

    def test_openpli_92_restores_native_list_and_removes_existing_canvas(self):
        # OpenPLi 9.2 has its own eListboxServiceContent implementation and
        # the OpenATV eCanvas above the list blacked out the entire list.
        # Simulate upgrading from TEST11 and running the skin customizer twice.
        original = BASE.read_text(encoding="utf-8")
        xml = (
            '    <widget source="ServiceEvent" render="WarderChannelEpgClip" '
            'position="60,96" size="1065,842" zPosition="4" '
            'warderProgressWidth="90" alphaTest="blend" transparent="1" />\\n'
        )
        end = original.find("</screen>", original.index('<screen name="ChannelSelection"'))
        seeded = original[:end] + xml + original[end:]
        tree = ast.parse(PLUGIN.read_text(encoding="utf-8"))
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "cChannelsel")
        def setting(value):
            return SimpleNamespace(value=value)
        config = SimpleNamespace(plugins=SimpleNamespace(
            setupGlass17=SimpleNamespace(
                par109=setting("#cdcdcd"), par110=setting("#6cbcf0"),
                par111=setting("#6cbcf0"), par117=setting("#dddddd")),
            warderEpgListScroll=SimpleNamespace(enabled=setting(False))))
        with TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "skin.xml"
            runtime.write_text(seeded, encoding="utf-8")
            scope = dict(config=config, SKINXML=str(runtime), ENA_P_CH=False,
                         isOpenPLi=True,
                         _atomicWriteText=lambda path, content: Path(path).write_text(content, encoding="utf-8"),
                         re=re, allow_channel_epg_overlay=lambda: True, allow_channel_epg_overlay=lambda: True)
            exec(compile(ast.Module(body=[fn], type_ignores=[]), str(PLUGIN), "exec"), scope)
            self.assertEqual(scope["cChannelsel"](), "c")
            changed = runtime.read_text(encoding="utf-8")
            screen = changed.split('<screen name="ChannelSelection"', 1)[1].split('</screen>', 1)[0]
            self.assertIn('<widget name="list"', screen)
            self.assertNotIn('render="WarderChannelEpgClip"', screen)
            self.assertIn('picServiceEventProgressbar=', screen)
            self.assertIn('serviceInfoFont=', screen)
            self.assertIn('render="WarderPrimeTime"', screen)
            self.assertIn('render="WarderPrimeTimeDivider"', screen)
            self.assertEqual(scope["cChannelsel"](), "c")
            self.assertEqual(runtime.read_text(encoding="utf-8"), changed)
            self.assertEqual(BASE.read_text(encoding="utf-8"), original)

    def test_openatv_keeps_approved_test11_event_overlay(self):
        original = BASE.read_text(encoding="utf-8")
        tree = ast.parse(PLUGIN.read_text(encoding="utf-8"))
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "cChannelsel")
        def setting(value):
            return SimpleNamespace(value=value)
        config = SimpleNamespace(plugins=SimpleNamespace(
            setupGlass17=SimpleNamespace(
                par109=setting("#cdcdcd"), par110=setting("#6cbcf0"),
                par111=setting("#6cbcf0"), par117=setting("#dddddd")),
            warderEpgListScroll=SimpleNamespace(enabled=setting(True))))
        with TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "skin.xml"
            runtime.write_text(original, encoding="utf-8")
            scope = dict(config=config, SKINXML=str(runtime), ENA_P_CH=False,
                         isOpenPLi=False,
                         _atomicWriteText=lambda path, content: Path(path).write_text(content, encoding="utf-8"),
                         re=re, allow_channel_epg_overlay=lambda: True, allow_channel_epg_overlay=lambda: True)
            exec(compile(ast.Module(body=[fn], type_ignores=[]), str(PLUGIN), "exec"), scope)
            self.assertEqual(scope["cChannelsel"](), "c")
            screen = runtime.read_text(encoding="utf-8").split(
                '<screen name="ChannelSelection"', 1)[1].split('</screen>', 1)[0]
            self.assertEqual(screen.count('render="WarderChannelEpgClip"'), 1)

    def test_description_and_event_rows_have_a_gap_and_other_screens_untouched(self):
        source = PLUGIN.read_text(encoding="utf-8")
        tree = ast.parse(source)
        fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                  and node.name == "cChannelsel")
        original = BASE.read_text(encoding="utf-8")

        def setting(value):
            return SimpleNamespace(value=value)

        config = SimpleNamespace(plugins=SimpleNamespace(
            setupGlass17=SimpleNamespace(
                par109=setting("#cdcdcd"), par110=setting("#6cbcf0"),
                par111=setting("#6cbcf0"), par117=setting("#dddddd")),
            warderEpgListScroll=SimpleNamespace(enabled=setting(True))))
        with TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "skin.xml"
            runtime.write_text(original, encoding="utf-8")
            output = []

            def write_text(path, text):
                self.assertEqual(Path(path), runtime)
                output.append(text)
                runtime.write_text(text, encoding="utf-8")

            scope = dict(config=config, SKINXML=str(runtime),
                         ENA_P_CH=False, _atomicWriteText=write_text, re=re, allow_channel_epg_overlay=lambda: True, allow_channel_epg_overlay=lambda: True)
            exec(compile(ast.Module(body=[fn], type_ignores=[]),
                         str(PLUGIN), "exec"), scope)
            self.assertEqual(scope["cChannelsel"](), "c")
            self.assertEqual(len(output), 1)
            # Reapplying the runtime customization must not stack overlays.
            self.assertEqual(scope["cChannelsel"](), "c")
            self.assertEqual(len(output), 2)
            self.assertEqual(output[-1].count('render="WarderChannelEpgClip"'), 1)
            changed = output[0]

        original_screen = original.split('<screen name="ChannelSelection"', 1)[1].split('</screen>', 1)[0]
        changed_screen = changed.split('<screen name="ChannelSelection"', 1)[1].split('</screen>', 1)[0]
        self.assertIn('position="1150,455"', changed_screen)
        self.assertIn('size="685,224"', changed_screen)
        self.assertIn('warderWholeLineScroll="1"', changed_screen)
        self.assertEqual(changed_screen.count('render="WarderChannelEpgClip"'), 1)
        self.assertIn('position="60,96" size="1065,842"', changed_screen)
        self.assertIn('warderProgressWidth="90"', changed_screen)
        self.assertIn('alphaTest="blend"', changed_screen)
        self.assertIn('position="1150,695" size="685,226"', changed_screen)
        # Default list should offer at most 6; larger fonts may fit fewer.
        self.assertIn('numEvents="6"', changed_screen)
        self.assertNotIn('numEvents="8"', changed_screen)
        self.assertNotIn('size="685,240"', changed_screen)
        self.assertNotIn('position="1150,685" size="685,236"', changed_screen)
        self.assertEqual(455 + 224, 679)
        self.assertGreaterEqual(695 - 679, 16)
        self.assertEqual(695 + 226, 921)
        # Original authored skin, configured fonts and unrelated screens untouched.
        self.assertEqual(BASE.read_text(encoding="utf-8"), original)
        self.assertEqual(original_screen.count('font="Prive4;25"'),
                         changed_screen.count('font="Prive4;25"'))
        # Ignore only the intentionally injected Prime Time footer font.
        # Existing user-configurable font declarations must stay intact.
        old_font_widgets = re.findall(r'<widget\\b[^>]*>', original_screen)
        new_font_widgets = [tag for tag in re.findall(r'<widget\\b[^>]*>', changed_screen)
                            if 'render="WarderPrimeTime"' not in tag]
        self.assertEqual(sum('font="Prive4;26"' in tag for tag in old_font_widgets),
                         sum('font="Prive4;26"' in tag for tag in new_font_widgets))
        # cChannelsel also adds existing margins to other ChannelSelection
        # variants; compare only unrelated menus for unintended changes.
        pattern = re.compile(r'<screen\\b[^>]*name="([^"]+)"[^>]*>.*?</screen>', re.S)
        def unrelated(text):
            return [(m.group(1), m.group(0)) for m in pattern.finditer(text)
                    if m.group(1) != "ChannelSelection"
                    and not m.group(1).startswith("ChannelSelection-")]
        self.assertEqual(unrelated(original), unrelated(changed))


if __name__ == "__main__":
    unittest.main()
