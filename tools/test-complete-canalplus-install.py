#!/usr/bin/env python3
"""Exercise the actual planner and installer against the full Canal+ ZIPs."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
spec = importlib.util.spec_from_file_location("sync", PKG / "warderPiconSync.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)
DELIVERY = ROOT / "assets/warder/downloads/picons/channels/test-candidate"
doc = json.loads((DELIVERY / "manifest.json").read_text())

# Extract actual production methods without importing the receiver GUI runtime.
names = {"_warderRunChannelQueue", "_warderInstallChannelArchive", "_warderRemoveStaleChannelPicons"}
tree = ast.parse((PKG / "plugin.py").read_bytes())
scope = dict(warderPiconSync=sync, os=os, shutil=shutil, tempfile=tempfile,
             zipfile=zipfile, stat=stat, _=lambda s: s)
methods = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name in names]
assert len(methods) == len(names)
for method in methods:
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(PKG / "plugin.py"), "exec"), scope)


class Receiver:
    _warderRunChannelQueue = scope["_warderRunChannelQueue"]
    _warderInstallChannelArchive = scope["_warderInstallChannelArchive"]
    _warderRemoveStaleChannelPicons = scope["_warderRemoveStaleChannelPicons"]

    def _warderLoadChannelManifest(self, url):
        assert url == sync.runtime_publication()["manifest_url"]
        return doc

    def _warderFetchChannelJob(self, job, target):
        data = (DELIVERY / job["filename"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == job["sha256"]
        assert len(data) == job["bytes"]
        Path(target).write_bytes(data)


def main():
    for style in ("transparent", "white", "black"):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "picon"
            destination.mkdir()
            receiver = Receiver()
            receiver.warderChannelQueue = None
            prefs = sync.set_task_position_bindings(sync.default_preferences(str(destination)),
                [sync.task_binding_for_package_selector(s) for s in ("CANALPLUS_CZ", "CANALPLUS_SK")])
            prefs.update(resolution="220x132", style=style, update_mode=sync.UPDATE_MODE_REPLACE_ALL, prepared=True)
            receiver.warderPiconPrefs = prefs
            # Existing transparent Jednotka must be replaced by black/white when requested.
            jedn = "1_0_1_3C3C_C90_3_EB0000_0_0_0.png"
            source = ROOT / ".approved-picons/picons/23.5e/canal-plus-sk"
            (destination / jedn).write_bytes((source / "transparent" / jedn).read_bytes())
            unrelated = destination / "1_0_1_1_1_1_C00000_0_0_0.png"
            unrelated.write_bytes(b"unchanged other orbital position")
            result = None
            for _iteration in range(4):
                result = receiver._warderRunChannelQueue()
                if result is not None:
                    break
            assert result is not None and "SUCCESSFUL" in result, result
            counts = {r["package_selector"]: r["updated"] for r in receiver.warderChannelPackageResults}
            assert counts == {"CANALPLUS_CZ": 231, "CANALPLUS_SK": 226}, counts
            assert not any(r["failures"] for r in receiver.warderChannelPackageResults)
            installed = {}
            for country in ("cz", "sk"):
                with zipfile.ZipFile(DELIVERY / ("canalplus_%s_%s_220x132.zip" % (country, style))) as archive:
                    for name in archive.namelist():
                        data = archive.read(name)
                        assert name not in installed or installed[name] == data, "conflicting SK/CZ identity"
                        installed[name] = data
                        assert (destination / name).read_bytes() == data
            assert (destination / jedn).read_bytes() == (source / style / jedn).read_bytes()
            assert unrelated.read_bytes() == b"unchanged other orbital position"
            print("PASS", style, counts, "unique installed", len(installed))


if __name__ == "__main__":
    main()
