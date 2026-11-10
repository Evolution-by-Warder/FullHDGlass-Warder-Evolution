#!/usr/bin/env python3
"""Exercise the actual production factory-icon restore function in isolation."""
import ast
import os
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py"
SOURCE = PLUGIN.read_text(encoding="utf-8")
FUNC = next(node for node in ast.parse(SOURCE).body
            if isinstance(node, ast.FunctionDef) and node.name == "restoreFactoryIcons")
code = compile(ast.Module(body=[FUNC], type_ignores=[]), str(PLUGIN), "exec")


class FactoryIconResetTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.factory = self.root / "icons_factory"
        self.live = self.root / "icons"
        self.factory.mkdir()
        self.live.mkdir()
        self.names = ("one", "two")
        self.scope = dict(os=os, shutil=shutil, SKINPATH=str(self.root),
                          allIcons=self.names)
        exec(code, self.scope)

    def test_all_runtime_icon_names_have_exactly_matching_factory_assets(self):
        module = ast.parse(SOURCE)
        declaration = next(
            node for node in module.body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "allIcons"
                    for target in node.targets)
        )
        names = ast.literal_eval(declaration.value)
        factory = ROOT / "source/package-root/usr/share/enigma2/hd_glass17/icons_factory"
        shipped = {path.stem for path in factory.glob("*.png")}
        self.assertEqual(len(names), 148)
        self.assertEqual(len(set(names)), 148)
        self.assertEqual(set(names), shipped)

    def test_restore_replaces_old_icons_offline(self):
        for name in self.names:
            (self.factory / (name + ".png")).write_bytes(("factory-" + name).encode())
            (self.live / (name + ".png")).write_bytes(b"old-selected-pack")
        self.assertTrue(self.scope["restoreFactoryIcons"]())
        for name in self.names:
            self.assertEqual((self.live / (name + ".png")).read_bytes(),
                             ("factory-" + name).encode())
            self.assertFalse((self.live / (name + ".png.warder-reset-tmp")).exists())

    def test_missing_factory_icon_does_not_partially_replace_existing_icons(self):
        (self.factory / "one.png").write_bytes(b"factory-one")
        for name in self.names:
            (self.live / (name + ".png")).write_bytes(b"original")
        self.assertFalse(self.scope["restoreFactoryIcons"]())
        for name in self.names:
            self.assertEqual((self.live / (name + ".png")).read_bytes(), b"original")

    def test_restore_when_default_icons_already_selected(self):
        for name in self.names:
            (self.factory / (name + ".png")).write_bytes(b"factory")
            (self.live / (name + ".png")).write_bytes(b"modified")
        self.assertTrue(self.scope["restoreFactoryIcons"]())
        self.assertEqual((self.live / "one.png").read_bytes(), b"factory")


if __name__ == "__main__":
    unittest.main()
