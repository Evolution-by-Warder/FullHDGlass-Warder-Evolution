"""Prime Time default ChannelSelection runtime layout regression tests.

Execute only the production cChannelsel function from AST: no Enigma2 runtime
or edits to packaged skin.xml. Covers toggling and repeated startup calls.
"""
import ast
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
SKIN = ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml"


def runtime_function(path, enabled):
    plugin_tree = ast.parse(PLUGIN.read_text(encoding="utf-8"))
    fn = next(x for x in plugin_tree.body
              if isinstance(x, ast.FunctionDef) and x.name == "cChannelsel")
    value = lambda x: SimpleNamespace(value=x)
    config = SimpleNamespace(plugins=SimpleNamespace(
        warderEvolutionPrimeTime=SimpleNamespace(enabled=value(enabled)),
        setupGlass17=SimpleNamespace(
            par109=value("#cdcdcd"), par110=value("#6cbcf0"),
            par111=value("#6cbcf0"), par117=value("#dddddd"))))
    context = {
        "config": config, "SKINXML": str(path), "ENA_P_CH": False,
        "_atomicWriteText": lambda p, content: Path(p).write_text(content, encoding="utf-8"),
    }
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(PLUGIN), "exec"), context)
    return context["cChannelsel"]


def channel_section(xml):
    return xml.split('<screen name="ChannelSelection"', 1)[1].split("</screen>", 1)[0]


class PrimeTimeRuntimeLayoutTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "skin.xml"
        self.original = SKIN.read_bytes()
        self.path.write_bytes(self.original)

    def run_layout(self, enabled):
        self.assertEqual(runtime_function(self.path, enabled)(), "c")
        return channel_section(self.path.read_text(encoding="utf-8"))

    def check_approved_regions(self, section):
        self.assertIn('render="WarderChannelEpgClip"', section)
        self.assertEqual(section.count('render="WarderChannelEpgClip"'), 1)
        self.assertIn('render="g17ShowExtraEpg"', section)
        self.assertIn('position="1150,695" size="685,226"', section)
        self.assertIn('numEvents="6"', section)
        self.assertIn('position="60,96"', section)

    def test_default_off_preserves_current_description_and_six_epg(self):
        section = self.run_layout(False)
        self.check_approved_regions(section)
        self.assertNotIn('render="WarderPrimeTime"', section)
        self.assertIn('position="1150,455"', section)
        self.assertIn('size="685,224"', section)
        self.assertEqual(SKIN.read_bytes(), self.original)

    def test_enabled_adds_footer_below_six_epg_without_moving_description(self):
        section = self.run_layout(True)
        self.assertIn('render="WarderChannelEpgClip"', section)
        self.assertIn('render="WarderPrimeTime" position="1150,898" size="685,38"', section)
        self.assertIn('position="1150,695" size="685,194"', section)
        self.assertIn('numEvents="6"', section)
        self.assertIn('render="g17MetrixHDRunningText"', section)
        self.assertIn('position="1150,455"', section)
        self.assertIn('size="685,224"', section)
        self.assertLessEqual(695 + 194, 898)
        self.assertLess(898 + 38, 943)
        self.assertEqual(SKIN.read_bytes(), self.original)

    def test_reopening_and_disabling_are_idempotent(self):
        first = self.run_layout(True)
        second = self.run_layout(True)
        self.assertIn('position="1150,695" size="685,194"', second)
        self.assertEqual(first, second)
        self.assertEqual(second.count('render="WarderPrimeTime"'), 1)
        reverted = self.run_layout(False)
        self.check_approved_regions(reverted)
        self.assertNotIn('render="WarderPrimeTime"', reverted)
        self.assertIn('position="1150,695" size="685,226"', reverted)
        self.assertIn('position="1150,455"', reverted)
        self.assertIn('size="685,224"', reverted)
        self.assertEqual(SKIN.read_bytes(), self.original)


if __name__ == "__main__":
    unittest.main()
