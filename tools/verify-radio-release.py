#!/usr/bin/env python3
"""Verify the release against the receiver-confirmed radio payload."""
import ast
import importlib.util
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "source/package-root"


def digest_graphics():
    approved = json.loads((ROOT/'design/settings-header-asset.json').read_text())
    header = PAYLOAD/approved['path']
    assert header.is_file() and hashlib.sha256(header.read_bytes()).hexdigest()==approved['sha256']
    additions=json.loads((ROOT/'design/settings-batch261-assets.json').read_text())['assets']
    pinned=set()
    prefix='usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/'
    for entry in additions:
        relative=entry['path']
        assert relative.startswith(prefix+'images/') or relative==prefix+'warder-infobar-types.zip'
        path=PAYLOAD/relative
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256'],relative
        pinned.add(path)
    assert {p for p in (PAYLOAD/prefix/'images').rglob('*.png')}=={p for p in pinned if p.suffix=='.png'}|{header}
    # Independently pinned spectrum-only frames. Keep every previously frozen
    # image and layout in the original digest; do not reset that baseline.
    spectrum=json.loads((ROOT/'design/radio-spectrum/frames.json').read_text())
    frame_root='usr/share/enigma2/hd_glass17/warder-spectrum/'
    expected={frame_root+'frame-%02d.png' % i for i in range(48)}
    assert {entry['path'] for entry in spectrum['assets']}==expected
    assert {path.relative_to(PAYLOAD).as_posix() for path in (PAYLOAD/frame_root).rglob('*') if path.is_file()}==expected
    for entry in spectrum['assets']:
        path=PAYLOAD/entry['path']
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
        pinned.add(path)
    keyboard=json.loads((ROOT/'design/virtual-keyboard/compatibility.json').read_text())
    keyboard_skin=PAYLOAD/'usr/share/enigma2/hd_glass17/skin.xml'
    for entry in keyboard['assets']:
        asset=PAYLOAD/entry['path']
        assert hashlib.sha256(asset.read_bytes()).hexdigest()==entry['sha256']
        assert hashlib.sha256((PAYLOAD/entry['source']).read_bytes()).hexdigest()==entry['source_sha256']
        pinned.add(asset)
    digest = hashlib.sha256()
    for path in sorted(PAYLOAD.rglob("*")):
        if path==header or path in pinned:continue  # Independently pinned settings-only addition; the radio baseline stays frozen.
        if path.is_file() and path.suffix.lower() in (".png", ".jpg", ".mvi", ".xml"):
            digest.update(path.relative_to(PAYLOAD).as_posix().encode() + b"\0")
            raw=path.read_bytes()
            if path==keyboard_skin:
                edits=ROOT/'design/openatv-compatibility/skin-edits.json'
                if edits.exists():
                    ledger=json.loads(edits.read_text())
                    text=raw.decode()
                    for edit in ledger['edits']:
                        assert text.count(edit['updated_screen'])==1
                        text=text.replace(edit['updated_screen'],edit['original_screen'],1)
                    raw=text.encode()
                    assert hashlib.sha256(raw).hexdigest()==ledger['before_skin_sha256']
                assert hashlib.sha256(raw).hexdigest()==keyboard['updated_skin_sha256']
                text=raw.decode()
                assert text.count(keyboard['updated_screen'])==1
                raw=text.replace(keyboard['updated_screen'],keyboard['original_screen'],1).encode()
                assert hashlib.sha256(raw).hexdigest()==keyboard['original_skin_sha256']
            digest.update(hashlib.sha256(raw).digest())
    return digest.hexdigest()


def main():
    baseline = json.loads((ROOT / "tools/radio-release-baseline.json").read_text())
    assert digest_graphics() == baseline["graphics_and_layout_sha256"]
    for path in PAYLOAD.rglob("*"):
        assert "__pycache__" not in path.parts and path.suffix not in (".pyc", ".pyo")
        if path.suffix == ".py":
            ast.parse(path.read_bytes(), filename=str(path))
    plugin_dir = PAYLOAD / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
    version = (plugin_dir / "version").read_text().strip()
    plugin = ast.parse((plugin_dir / "plugin.py").read_bytes())
    order = next(node for node in ast.walk(plugin) if isinstance(node, ast.FunctionDef) and node.name == "_warderVersionTuple")
    scope = {"re": re}
    exec(compile(ast.Module(body=[order], type_ignores=[]), "version_order", "exec"), scope)
    compare = lambda value: scope["_warderVersionTuple"](None, value)
    assert compare("1.0.4") < compare("1.0.5-test250") < compare(version)
    for name in ("preinst", "postinst", "postrm"):
        path = ROOT / "source/control" / name
        subprocess.run(["sh", "-n", str(path)], check=True)
        assert path.stat().st_mode & 0o111 == 0o111
    package_id = next(line.split(":",1)[1].strip() for line in (ROOT/"source/control/control").read_text().splitlines() if line.startswith("Package:"))
    prefix = "enigma2-plugin-skins-fullhdglass" if package_id == "enigma2-plugin-skins-fullhdglass-warder-evolution" else "enigma2-skin-fullhdglass-warder-evolution"
    package = ROOT / "packages" / (prefix+"_%s_all.ipk" % version)
    if package.is_file():
        assert subprocess.check_output(["ar", "p", str(package), "debian-binary"]) == b"2.0\n"
        data = subprocess.check_output(["ar", "p", str(package), "data.tar.gz"])
        optimizer_spec = importlib.util.spec_from_file_location("png_optimizer", ROOT / "tools/optimize-png.py")
        optimizer = importlib.util.module_from_spec(optimizer_spec)
        optimizer_spec.loader.exec_module(optimizer)
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            files = {entry.name.removeprefix("./"): entry for entry in archive if entry.isfile()}
            expected = {path.relative_to(PAYLOAD).as_posix(): path for path in PAYLOAD.rglob("*") if path.is_file() and path.suffix != ".po"}
            assert files.keys() == expected.keys()
            for name, path in expected.items():
                raw = path.read_bytes()
                expected_raw = optimizer.optimize(raw) if path.suffix == ".png" else raw
                assert archive.extractfile(files[name]).read() == expected_raw, name
                if path.suffix == ".py":
                    assert files[name].mtime == (int(hashlib.sha256(path.read_bytes()).hexdigest()[:8], 16) & 0x7fffffff)
        digest = hashlib.sha256(package.read_bytes()).hexdigest()
        feed_names=("update-production.json", "update-test.json") if package_id=="enigma2-plugin-skins-fullhdglass-warder-evolution" else ("update.json", "update-test.json")
        for name in feed_names:
            manifest = json.loads((ROOT / name).read_text())
            assert manifest["version"] == version and manifest["sha256"] == digest
            assert manifest["package_url"].rsplit("/",1)[0].endswith("/main/packages")
            assert manifest["package_url"].rsplit("/",1)[-1] in (package.name,"enigma2-plugin-skins-fullhdglass_"+version+"_all.ipk")
    print("PASS: pinned graphics/layout, Python syntax, executable hooks, version order, full IPK and matching stable/native TEST manifests")


if __name__ == "__main__":
    main()
