"""Simulate the default ChannelSelection runtime geometry patch without Enigma2.

Receiver QA identified a real 10px intersection between description and
upcoming EPG. Only a generated runtime skin may be adjusted; never the
approved source skin.xml or user font sizes.
"""
import ast
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

    def test_description_and_event_rows_have_a_gap_and_other_screens_untouched(self):
        source = PLUGIN.read_text(encoding="utf-8")
        tree = ast.parse(source)
        fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                  and node.name == "cChannelsel")
        original = BASE.read_text(encoding="utf-8")

        def setting(value):
            return SimpleNamespace(value=value)

        config = SimpleNamespace(plugins=SimpleNamespace(setupGlass17=SimpleNamespace(
            par109=setting("#cdcdcd"), par110=setting("#6cbcf0"),
            par111=setting("#6cbcf0"), par117=setting("#dddddd"))))
        with TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "skin.xml"
            runtime.write_text(original, encoding="utf-8")
            output = []

            def write_text(path, text):
                self.assertEqual(Path(path), runtime)
                output.append(text)
                runtime.write_text(text, encoding="utf-8")

            scope = dict(config=config, SKINXML=str(runtime),
                         ENA_P_CH=False, _atomicWriteText=write_text)
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
        self.assertEqual(original_screen.count('font="Prive4;26"'),
                         changed_screen.count('font="Prive4;26"'))
        # cChannelsel also adds existing margins to other ChannelSelection
        # variants; compare only unrelated menus for unintended changes.
        import re
        pattern = re.compile(r'<screen\\b[^>]*name="([^"]+)"[^>]*>.*?</screen>', re.S)
        def unrelated(text):
            return [(m.group(1), m.group(0)) for m in pattern.finditer(text)
                    if m.group(1) != "ChannelSelection"
                    and not m.group(1).startswith("ChannelSelection-")]
        self.assertEqual(unrelated(original), unrelated(changed))


if __name__ == "__main__":
    unittest.main()
