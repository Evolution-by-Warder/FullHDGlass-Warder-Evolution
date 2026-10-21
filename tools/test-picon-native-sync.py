#!/usr/bin/env python3
"""Exercise the real downloader and selective PNG installer against publication."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"


def main():
    spec = importlib.util.spec_from_file_location("sync", PKG / "warderPiconSync.py")
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    url = sync.runtime_publication()["manifest_url"]
    with urlopen(url, timeout=60) as response:
        doc = json.load(response)
    names = ["1_0_1_3C3C_C90_3_EB0000_0_0_0", "1_0_16_5318_C96_3_EB0000_0_0_0",
             "1_0_1_335B_C93_3_EB0000_0_0_0"]
    queue = dict(package_selectors=["235E"], positions=["23.5e"],
        position_bindings=[sync.task_binding_for_package_selector("235E")],
        resolution="220x132", style="black", mode=sync.UPDATE_MODE_SYNC_TV,
        services=[dict(service_reference=name, position="23.5e") for name in names], manifest_url=url)
    plan = sync.plan_runtime_packages(doc, queue, url)
    jobs = sync.build_download_jobs(doc, plan, url)
    assert jobs["state"] == "ready" and len(jobs["jobs"]) == 1
    job = jobs["jobs"][0]
    assert job["family"] == "channel-black"
    scope = dict(warderPiconSync=sync, hashlib=hashlib, Request=Request, urlopen=urlopen,
                 os=os, tempfile=tempfile, shutil=shutil, stat=stat, zipfile=zipfile)
    tree = ast.parse((PKG / "plugin.py").read_bytes())
    for name in ("_warderFetchChannelJob", "_warderInstallChannelArchive"):
        method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)
        exec(compile(ast.Module(body=[method], type_ignores=[]), "plugin.py", "exec"), scope)
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        archive = root / "package.zip"
        destination = root / "picon"
        destination.mkdir()
        for name in names:
            (destination / (name + ".png")).write_bytes(b"old transparent PNG")
        scope["_warderFetchChannelJob"](None, job, str(archive))
        wanted = sync.wanted_picon_names(queue)
        installed, available = scope["_warderInstallChannelArchive"](None, str(archive), str(destination), wanted)
        assert installed == wanted and len(installed) == 3
        assert {p.name for p in destination.iterdir()} == wanted
        expected = {
            names[1]: "b0f744945100b31623bf667c26b0fa9b421c14b5afd13d09e8b205b6d558d3a5",
            names[2]: "329d977f16960b0de17342e862b8507706db65bdfd46a52093d0016d0bc1d6c0",
        }
        for name, digest in expected.items():
            assert hashlib.sha256((destination / (name + ".png")).read_bytes()).hexdigest() == digest
        print("PASS: actual network download with all hashes verified; 3 selected PNGs installed from %d; approved black Osem and Seznam" % len(available))


if __name__ == "__main__":
    main()
