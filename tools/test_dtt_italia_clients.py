"""Exercise both receiver installers against the same candidate files on disk."""
import argparse
import ast
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import types
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
RECIPE = ROOT / "reports/dtt-italia-20261123/recipe.json"


def check(clients, channels, report):
    package = types.ModuleType("dtt_hub")
    package.__path__ = [str(clients / "plugin/src/Plugins/Extensions/WarderPiconHub")]
    sys.modules[package.__name__] = package
    from dtt_hub import warder_engine as engine
    spec = importlib.util.spec_from_file_location("dtt_skin", NATIVE / "warderPiconSync.py")
    skin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(skin)
    source = ast.parse((NATIVE / "plugin.py").read_bytes())
    node = next(n for n in ast.walk(source) if isinstance(n, ast.FunctionDef) and n.name == "_warderInstallChannelArchive")
    scope = dict(warderPiconSync=skin, os=os, shutil=shutil, stat=stat, tempfile=tempfile, zipfile=zipfile)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(NATIVE / "plugin.py"), "exec"), scope)
    refs = json.loads(RECIPE.read_bytes())["selectors"]
    body = (channels / "manifest.json").read_bytes()
    document = json.loads(body)
    proof = []
    for sync in (skin, engine.sync):
        assert not sync.validate_publication_manifest(document)
        assert sync.namespace_to_orbital_position("EEEE0272") == "dtt"
        assert sync.task_binding_for_display_label("DTT ITALIA")["package_selector"] == "DTT_ITALIA"
    def opener(url):
        if url == engine.sync.RUNTIME_MANIFEST_URL:
            return io.BytesIO(body)
        return (channels / url.rsplit("/", 1)[1]).open("rb")
    for p in document["packages"]:
        selector, size, style = p["selector_id"], p["resolution"], p["family"][8:]
        if selector not in refs:
            continue
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            archive = root / "input.zip"
            with archive.open("wb") as out:
                for url in p["parts"]:
                    with opener(url) as chunk:
                        shutil.copyfileobj(chunk, out)
            assert hashlib.sha256(archive.read_bytes()).hexdigest() == p["sha256"]
            with zipfile.ZipFile(archive) as z:
                wanted = {r + ".png" for r in refs[selector]}
                assert wanted <= set(z.namelist())
                dest = root / "skin"
                dest.mkdir()
                installed, available = scope[node.name](None, str(archive), str(dest), wanted=wanted)
                assert installed == wanted and wanted <= available
                assert all((dest / n).read_bytes() == z.read(n) for n in wanted)
                ref = next(r for r in sorted(refs[selector]) if r.split("_")[2] != "2")
                enigma = root / "enigma2"
                enigma.mkdir()
                (enigma / "bouquets.tv").write_text('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.it.tv" ORDER BY bouquet\n')
                (enigma / "userbouquet.it.tv").write_text("#NAME Italia\n#SERVICE " + ref.replace("_", ":") + ":\n")
                for sync in (skin, engine.sync):
                    binding = sync.task_binding_for_package_selector(selector)
                    prefs = sync.set_task_position_bindings(sync.default_preferences(), [binding])
                    prefs.update(resolution=size, style=style, update_mode=sync.UPDATE_MODE_SYNC_TV)
                    plan = sync.plan_runtime_packages(document, sync.build_runtime_queue(prefs, enigma2_dir=str(enigma)))
                    jobs = sync.build_download_jobs(document, plan)
                    assert jobs["state"] == "ready" and [j["selector_id"] for j in jobs["jobs"]] == [selector]
                for mode in (engine.sync.UPDATE_MODE_SYNC_TV, engine.sync.UPDATE_MODE_INCREMENTAL):
                    dest = root / mode
                    dest.mkdir()
                    foreign = dest / "1_0_1_ABCD_ABC_AB_EEEE0000_0_0_0.png"
                    foreign.write_bytes(b"local")
                    prefs.update(update_mode=mode, destination=str(dest))
                    runner = engine.PiconRunner(opener=opener, enigma2_dir=str(enigma), lock_path=str(root / "lock"))
                    runner.run([prefs])
                    names = wanted if mode == engine.sync.UPDATE_MODE_INCREMENTAL else {ref + ".png"}
                    assert all((dest / n).read_bytes() == z.read(n) for n in names)
                    if mode == engine.sync.UPDATE_MODE_SYNC_TV:
                        assert {p.name for p in dest.glob("*.png")} == names | {foreign.name}
                    assert foreign.read_bytes() == b"local"
                proof.append([selector, size, style])
    assert len(proof) == 27
    report.write_text(json.dumps({"verified": proof, "fullhdglass_installs": len(proof),
                                 "hub_installs": len(proof)*2, "plans": len(proof)*2,
                                 "physical_receiver": False}, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hub", type=Path, required=True)
    parser.add_argument("--channels", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    check(args.hub, args.channels, args.report)
