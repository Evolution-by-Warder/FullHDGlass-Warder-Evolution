#!/usr/bin/env python3
"""Verify the release against the receiver-confirmed radio payload."""
import ast
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
    digest = hashlib.sha256()
    for path in sorted(PAYLOAD.rglob("*")):
        if path.is_file() and path.suffix.lower() in (".png", ".jpg", ".mvi", ".xml"):
            digest.update(path.relative_to(PAYLOAD).as_posix().encode() + b"\0")
            digest.update(hashlib.sha256(path.read_bytes()).digest())
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
    package = ROOT / "packages" / ("enigma2-skin-fullhdglass17-warder-evolution_%s_all.ipk" % version)
    if package.is_file():
        assert subprocess.check_output(["ar", "p", str(package), "debian-binary"]) == b"2.0\n"
        data = subprocess.check_output(["ar", "p", str(package), "data.tar.gz"])
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            files = {entry.name.removeprefix("./"): entry for entry in archive if entry.isfile()}
            expected = {path.relative_to(PAYLOAD).as_posix(): path for path in PAYLOAD.rglob("*") if path.is_file() and path.suffix != ".po"}
            assert files.keys() == expected.keys()
            for name, path in expected.items():
                assert archive.extractfile(files[name]).read() == path.read_bytes(), name
                if path.suffix == ".py":
                    assert files[name].mtime == (int(hashlib.sha256(path.read_bytes()).hexdigest()[:8], 16) & 0x7fffffff)
        digest = hashlib.sha256(package.read_bytes()).hexdigest()
        for name in ("update.json", "update-test.json"):
            manifest = json.loads((ROOT / name).read_text())
            assert manifest["version"] == version and manifest["sha256"] == digest
            assert manifest["package_url"].endswith("/main/packages/" + package.name)
    print("PASS: confirmed graphics/layout, Python syntax, executable hooks, version order, full IPK and both update manifests")


if __name__ == "__main__":
    main()
