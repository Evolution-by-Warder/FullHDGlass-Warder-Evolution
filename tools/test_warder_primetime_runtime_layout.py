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

    def test_default_off_preserves_six_full_epg_slots(self):
        section = self.run_layout(False)
        self.check_approved_regions(section)
        self.assertIn('render="WarderPrimeTimeDivider" position="1150,892" size="685,1"', section)
        self.assertIn('render="WarderPrimeTime" position="1150,898" size="685,38"', section)
        self.assertNotIn('<eLabel position="1150,892"', section)
        self.assertIn('numEvents="6"', section)
        self.assertIn('position="1150,455"', section)
        self.assertIn('size="685,224"', section)
        self.assertEqual(SKIN.read_bytes(), self.original)

    def test_enabled_uses_five_events_and_bottom_prime_time_dynamically(self):
        section = self.run_layout(True)
        self.check_approved_regions(section)
        self.assertIn('render="WarderPrimeTime" position="1150,898" size="685,38"', section)
        self.assertIn('render="WarderPrimeTimeDivider" position="1150,892" size="685,1"', section)
        self.assertEqual(section.count('render="WarderPrimeTimeDivider"'), 1)
        self.assertEqual(section.count('render="WarderPrimeTime"'), 1)
        self.assertIn('position="1150,695" size="685,226"', section)
        self.assertIn('numEvents="6"', section)
        self.assertIn('render="g17MetrixHDRunningText"', section)
        self.assertIn('position="1150,455"', section)
        self.assertIn('size="685,224"', section)
        self.assertLessEqual(695 + 226, 943)
        self.assertLess(898 + 38, 943)
        self.assertEqual(SKIN.read_bytes(), self.original)

    def test_reopening_toggle_keeps_same_full_six_row_xml(self):
        enabled = self.run_layout(True)
        self.check_approved_regions(enabled)
        self.assertEqual(self.run_layout(True), enabled)
        self.assertEqual(enabled.count('render="WarderPrimeTimeDivider"'), 1)
        self.assertEqual(enabled.count('render="WarderPrimeTime"'), 1)
        disabled = self.run_layout(False)
        self.check_approved_regions(disabled)
        self.assertEqual(disabled, enabled)
        self.assertEqual(self.run_layout(False), disabled)
        self.assertEqual(self.run_layout(True), enabled)
        self.assertEqual(SKIN.read_bytes(), self.original)

    def test_renderers_follow_live_switch_without_recreating_screen(self):
        import ast
        import types
        from unittest.mock import patch
        from pathlib import Path
        extra = (ROOT / "source/package-root/usr/lib/enigma2/python/Components/Renderer/g17ShowExtraEpg.py").read_text()
        divider_source = (ROOT / "source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderPrimeTimeDivider.py").read_text()
        self.assertIn("visible_events = min(self.numEvents, 5 if prime_enabled else 6)", extra)
        tree = ast.parse(divider_source)
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "WarderPrimeTimeDivider")
        changed = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "changed")
        enabled = SimpleNamespace(value=False)
        fake_config = SimpleNamespace(plugins=SimpleNamespace(
            warderEvolutionPrimeTime=SimpleNamespace(enabled=enabled)))
        scope = {"config": fake_config}
        exec(compile(ast.Module(body=[changed], type_ignores=[]), "divider", "exec"), scope)
        calls = []
        widget = SimpleNamespace(instance=SimpleNamespace(
            show=lambda: calls.append("show"), hide=lambda: calls.append("hide")),
            CHANGED_CLEAR=1)
        scope["changed"](widget, (0,))
        enabled.value = True
        scope["changed"](widget, (0,))
        enabled.value = False
        scope["changed"](widget, (0,))
        self.assertEqual(calls, ["hide", "show", "hide"])


if __name__ == "__main__":
    unittest.main()
