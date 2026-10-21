#!/usr/bin/env python3
"""Reproduce the stale-bytecode upgrade and verify packaging and hook fixes."""
import importlib.util
import io
import os
from pathlib import Path
import py_compile
import shlex
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder", ROOT / "tools/build-release-ipk.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def imported(path):
    spec = importlib.util.spec_from_file_location("test_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.CATALOGUE


def test_upgrade():
    old = b"CATALOGUE = '" + b"a" * 40 + b"'\n"
    new = b"CATALOGUE = '" + b"b" * 40 + b"'\n"
    assert len(old) == len(new)
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        legacy = root / "legacy.py"
        legacy.write_bytes(old)
        os.utime(legacy, (0, 0))
        py_compile.compile(str(legacy), doraise=True)
        legacy.write_bytes(new)
        os.utime(legacy, (0, 0))
        assert imported(legacy) == "a" * 40, "the original failure must reproduce"
        source = root / "source"
        source.mkdir()
        path = source / "module.py"
        built = []
        for number, content in enumerate((old, new)):
            path.write_bytes(content)
            package = root / ("package%d.tar.gz" % number)
            builder.archive(source, package, payload=True)
            repeated = root / ("repeat%d.tar.gz" % number)
            builder.archive(source, repeated, payload=True)
            assert package.read_bytes() == repeated.read_bytes()
            with tarfile.open(fileobj=io.BytesIO(package.read_bytes()), mode="r:gz") as archive:
                entry = archive.getmember("./module.py")
                built.append((archive.extractfile(entry).read(), entry.mtime))
        assert built[0][1] != built[1][1]
        installed = root / "installed.py"
        installed.write_bytes(built[0][0])
        os.utime(installed, (built[0][1], built[0][1]))
        py_compile.compile(str(installed), doraise=True)
        installed.write_bytes(built[1][0])
        os.utime(installed, (built[1][1], built[1][1]))
        assert imported(installed) == "b" * 40


def test_hook():
    text = (ROOT / "source/control/postinst").read_text()
    block = text[text.index("# Invalidate bytecode"):text.index("# Apply the selected InfoBar")]
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        source = root / "warderPiconSync.py"
        source.write_text("CATALOGUE = 'current'\n")
        cache = root / "__pycache__"
        cache.mkdir()
        obsolete = [root / "warderPiconSync.pyc", root / "warderPiconSync.pyo",
                    cache / "warderPiconSync.cpython-312.pyc"]
        for path in obsolete:
            path.write_bytes(b"obsolete")
        user_cache = cache / "user_custom.cpython-312.pyc"
        user_cache.write_bytes(b"preserve unrelated module")
        block = block.replace("warder_python=/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17",
                              "warder_python=" + shlex.quote(str(root)))
        subprocess.run(["sh", "-eu", "-c", block], check=True)
        assert all(not path.exists() for path in obsolete)
        assert source.read_text() == "CATALOGUE = 'current'\n"
        assert user_cache.read_bytes() == b"preserve unrelated module"


def test_error_details():
    path = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py"
    spec = importlib.util.spec_from_file_location("sync", path)
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    summary = sync.package_result_summary([dict(selector_id="235E", orbital_position="23.5e",
        updated=0, failures=1, error="Warder channel part integrity mismatch\nwith details")])
    assert summary["failures"] == 1 and summary["updated"] == 0
    assert "ERROR: Warder channel part integrity mismatch with details" in summary["text"]
    good = sync.package_result_summary([dict(selector_id="235E", updated=3, failures=0)])
    assert good["status"] == "SUCCESSFUL" and good["updated"] == 3


if __name__ == "__main__":
    test_upgrade()
    test_hook()
    test_error_details()
    print("PASS: stale import reproduced; equal-size upgrade loads new code; deterministic packages; scoped cleanup; failure reason displayed")
