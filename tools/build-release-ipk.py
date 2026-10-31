#!/usr/bin/env python3
"""Package the approved, checked-in payload without regenerating its artwork."""
import gzip
import hashlib
import io
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def archive(directory, output, payload=False):
    with output.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.GNU_FORMAT) as tar:
            for path in sorted(directory.rglob("*")):
                if "__pycache__" in path.parts or path.suffix in (".pyc", ".pyo"):
                    raise SystemExit("Bytecode must not be packaged: %s" % path)
                # Translation sources stay in Git; ship the receiver-confirmed MO files.
                if payload and path.suffix == ".po":
                    continue
                entry = tar.gettarinfo(str(path), arcname="./" + path.relative_to(directory).as_posix())
                entry.uid = entry.gid = entry.mtime = 0
                entry.uname = entry.gname = ""
                if entry.isfile():
                    data = path.read_bytes()
                    if payload and path.suffix == ".py":
                        # A constant mtime and an unchanged source length can
                        # validate stale bytecode after a package upgrade.
                        # Keep builds reproducible while invalidating that cache.
                        entry.mtime = int(hashlib.sha256(data).hexdigest()[:8], 16) & 0x7fffffff
                    tar.addfile(entry, io.BytesIO(data))
                else:
                    tar.addfile(entry)


def main():
    payload = ROOT / "source/package-root"
    from sync_header_version import sync_headers
    sync_headers(payload, check=True)
    control = ROOT / "source/control"
    version = (payload / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/version").read_text().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit("A stable release version is required")
    metadata = (control / "control").read_text()
    package_id = next(line.split(":",1)[1].strip() for line in metadata.splitlines() if line.startswith("Package:"))
    assert package_id in ("enigma2-skin-fullhdglass17", "enigma2-plugin-skins-fullhdglass-warder-evolution")
    assert "Version: %s-1\n" % version in metadata
    for name in ("preinst", "postinst", "postrm"):
        assert (control / name).stat().st_mode & 0o111 == 0o111
    prefix = "enigma2-plugin-skins-fullhdglass" if package_id == "enigma2-plugin-skins-fullhdglass-warder-evolution" else "enigma2-skin-fullhdglass-warder-evolution"
    output = ROOT / "packages" / (prefix+"_%s_all.ipk" % version)
    output.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as work:
        work = Path(work)
        (work / "debian-binary").write_bytes(b"2.0\n")
        archive(control, work / "control.tar.gz")
        archive(payload, work / "data.tar.gz", payload=True)
        subprocess.run(["ar", "rcsD", str(output), "debian-binary", "control.tar.gz", "data.tar.gz"], cwd=work, check=True)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(digest + "  " + output.name + "\n")
    print(output)
    print(digest)


if __name__ == "__main__":
    main()
