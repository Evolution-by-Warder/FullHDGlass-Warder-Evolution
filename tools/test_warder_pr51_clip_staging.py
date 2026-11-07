"""Ensure isolated TEST54 staging alters only its temporary payload."""
import importlib.util
import re
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml"
STAGER = ROOT / "tools/stage-pr51-clip-candidate.py"


def load_stager():
    spec = importlib.util.spec_from_file_location("pr51_staging", STAGER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.stage_skin


class StagingTests(unittest.TestCase):
    def test_opt_in_receiver_progress_geometry_and_marker_are_isolated(self):
        original = BASE.read_text(encoding="utf-8")
        with TemporaryDirectory() as directory:
            target = Path(directory) / "skin.xml"
            target.write_text(original, encoding="utf-8")
            changed = load_stager()(target, progress_width=90, marker=True)
            self.assertIn('warderProgressWidth="90"', changed)
            self.assertIn('warderTestMarker="1"', changed)
            self.assertIn('position="1000,102" size="44,12"', changed)
            self.assertIn('backgroundColor="#00ff00" zPosition="20"', changed)
            self.assertEqual(changed.count('render="WarderChannelEpgClip"'), 1)
        self.assertEqual(BASE.read_text(encoding="utf-8"), original)

    def test_default_screen_only_and_no_font_modification(self):
        original = BASE.read_text(encoding="utf-8")
        with TemporaryDirectory() as directory:
            target = Path(directory) / "skin.xml"
            target.write_text(original, encoding="utf-8")
            rendered = load_stager()(target)
            self.assertEqual(rendered, target.read_text(encoding="utf-8"))
            self.assertEqual(rendered.count('render="WarderChannelEpgClip"'), 1)
            with self.assertRaisesRegex(RuntimeError, "already contains"):
                load_stager()(target)
        self.assertEqual(BASE.read_text(encoding="utf-8"), original)
        pattern = re.compile(r'<screen\b[^>]*name="([^"]+)"[^>]*>.*?</screen>', re.S)
        old = {m.group(1): m.group(0) for m in pattern.finditer(original)}
        updated = {m.group(1): m.group(0) for m in pattern.finditer(rendered)}
        self.assertEqual(old.keys(), updated.keys())
        for name in old:
            if name != "ChannelSelection":
                self.assertEqual(old[name], updated[name], name)
        default = updated["ChannelSelection"]
        self.assertIn('warderWholeLineScroll="1"', default)
        self.assertIn('size="685,224"', default)
        self.assertIn('position="1150,695" size="685,226"', default)
        self.assertIn('numEvents="6"', default)
        self.assertNotIn('numEvents="8"', default)
        self.assertIn('fieldMargins="26"', default)
        self.assertEqual(455 + 224 + 16, 695)
        self.assertNotIn('size="685,240"', default)
        self.assertNotIn('position="1150,685" size="685,236"', default)
        for font in ('Prive4;33', 'Prive4;30', 'Prive4;25', 'Prive4;26'):
            self.assertEqual(old["ChannelSelection"].count(font), default.count(font))


if __name__ == "__main__":
    unittest.main()
