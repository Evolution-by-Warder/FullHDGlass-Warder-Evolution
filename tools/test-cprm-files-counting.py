#!/usr/bin/env python3
"""Regression for truthful auxiliary-PNG copy counts in plugin.cprmFiles."""
import ast
import hashlib
import importlib.util
import os
import shutil
import tempfile
from types import SimpleNamespace
from unittest import mock


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN = os.path.join(
    ROOT,
    "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py",
)


class CopyHarness:
    def __init__(self, archive_root, destination_root):
        self.zzz = archive_root + os.sep
        self.enaSelectsat = False
        self.removed = False
        self.config = SimpleNamespace(
            plugins=SimpleNamespace(
                setupGlass17=SimpleNamespace(par39=SimpleNamespace(value=destination_root))
            )
        )

    def rmTmp2(self, _root, _folder):
        self.removed = True

    def _warderFilesMatch(self, source, destination):
        def digest(path):
            hasher = hashlib.sha256()
            with open(path, "rb") as stream:
                for chunk in iter(lambda: stream.read(65536), b""):
                    hasher.update(chunk)
            return hasher.digest()

        return os.path.getsize(source) == os.path.getsize(destination) and digest(source) == digest(destination)


with open(PLUGIN, "r", encoding="utf-8") as source_file:
    module = ast.parse(source_file.read(), filename=PLUGIN)
plugin_class = next(
    node for node in module.body
    if isinstance(node, ast.ClassDef)
    and any(isinstance(item, ast.FunctionDef) and item.name == "cprmFiles" for item in node.body)
)
method = next(
    node for node in plugin_class.body if isinstance(node, ast.FunctionDef) and node.name == "cprmFiles"
)
isolated = ast.Module(body=[method], type_ignores=[])
ast.fix_missing_locations(isolated)
namespace = {"os": os, "shutil": shutil, "listDir": os.listdir, "fileExists": os.path.exists}
exec(compile(isolated, PLUGIN, "exec"), namespace)
cprm_files = namespace["cprmFiles"]

with tempfile.TemporaryDirectory(prefix="cprm-files-") as temporary:
    archive_root = os.path.join(temporary, "download")
    destination_root = os.path.join(temporary, "receiver")
    archive = os.path.join(archive_root, "piconProv")
    destination = os.path.join(destination_root, "piconProv")
    os.makedirs(archive)
    os.makedirs(destination)
    with open(os.path.join(archive, "copied.png"), "wb") as stream:
        stream.write(b"fresh picon bytes")
    with open(os.path.join(archive, "failed.png"), "wb") as stream:
        stream.write(b"new bytes which must not be reported")
    with open(os.path.join(archive, "about.txt"), "w", encoding="utf-8") as stream:
        stream.write("metadata is not a picon")
    with open(os.path.join(destination, "failed.png"), "wb") as stream:
        stream.write(b"stale old picon")

    real_copy2 = shutil.copy2

    def fail_one_current_copy(source, target):
        if os.path.basename(source) == "failed.png":
            raise OSError("simulated disk write failure")
        return real_copy2(source, target)

    harness = CopyHarness(archive_root, destination_root)
    namespace["config"] = harness.config
    with mock.patch.object(shutil, "copy2", side_effect=fail_one_current_copy):
        updated, attempts = cprm_files(harness, "piconProv")

    assert (updated, attempts) == (1, 2), (updated, attempts)
    with open(os.path.join(destination, "failed.png"), "rb") as stream:
        assert stream.read() == b"stale old picon"
    assert harness.removed

print("PASS: successful write counted; failed current copy and stale destination not counted; non-PNG ignored")

SYNC = os.path.join(
    ROOT,
    "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py",
)
spec = importlib.util.spec_from_file_location("warderPiconSync_result_status", SYNC)
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)
summary = sync.package_result_summary([
    {"orbital_position": "16.0E", "package_selector": "160E", "updated": 12, "failures": 0},
    {"orbital_position": "23.5E", "package_selector": "235E", "updated": 4, "failures": 1},
])
rows = summary["text"].splitlines()
assert rows[0].startswith("SUCCESSFUL: 16.0E / "), rows[0]
assert rows[1].startswith("PARTIAL SUCCESS: 23.5E / "), rows[1]
assert rows[2].startswith("PARTIAL SUCCESS: Total: 16 picons updated"), rows[2]
assert rows[3] == "ERROR: Failures: 1", rows[3]
assert summary["status"] == "PARTIAL SUCCESS"

with open(PLUGIN, "r", encoding="utf-8") as plugin_file:
    plugin_source = plugin_file.read()
assert 'Label(_("Close") if self.res else _("Cancel"))' in plugin_source
assert 'elif _("ERROR") in x or _("PARTIAL SUCCESS") in x:' in plugin_source
print("PASS: result rows and summaries carry per-row status; partial results are not green")
