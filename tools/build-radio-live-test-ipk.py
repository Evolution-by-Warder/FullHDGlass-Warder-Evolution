#!/usr/bin/env python3
"""Build a receiver-installable FullHDGlass RADIO LIVE test IPK.

Never modifies committed source, production version, releases or update feeds.
Only the temporary TAR member for the version file is marked as test.
"""
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/package-root"
CONTROL = ROOT / "source/control"
OUT_DIR = ROOT / "packages/radio-live-test"
RUNTIME_VERSION = "1.0.81-test128"
PACKAGE_VERSION = RUNTIME_VERSION + "-1"
PKG_NAME = "enigma2-plugin-skins-fullhdglass"
PACKAGE_ID = "enigma2-plugin-skins-fullhdglass-warder-evolution"
PLUGIN = "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
VERSION_REL = PLUGIN + "/version"
REQUIRED = {
    PLUGIN + "/warderRadioLive.py",
    PLUGIN + "/warderRadioUpdate.py",
    PLUGIN + "/warderChannelPicons.py",
    PLUGIN + "/plugin.py",
    VERSION_REL,
}
BLOCKED_GRAPHICS = {
    "warder_gsu.png", "warder_piconhub.png",
    "warder_radio.png", "warder_youtube.png",
}


def check_sources():
    text = (CONTROL / "control").read_text(encoding="utf-8")
    version = (SOURCE / VERSION_REL).read_text(encoding="utf-8").strip()
    assert "Package: " + PACKAGE_ID + "\n" in text, "Unexpected installed package ID"
    assert "Version: 1.0.80-1\n" in text, "Base package version changed; re-evaluate upgrade safety"
    assert version == "1.0.80", "Base runtime changed; re-evaluate upgrade safety"
    for name in REQUIRED:
        if not (SOURCE / name).is_file():
            raise RuntimeError("Required test payload missing: " + name)
    if not (CONTROL / "postinst").is_file() or not (CONTROL / "preinst").is_file():
        raise RuntimeError("Missing native package installer scripts")
    # The bridge must not be published as a complete feature before its native
    # receiver test. This packager never writes a release feed or production IPK.
    return text.replace("Version: 1.0.80-1\n",
                        "Version: " + PACKAGE_VERSION + "\n").replace(
        "Description: FullHDGlass - Warder Evolution - modern Enigma2 skin continuation",
        "Description: FullHDGlass Warder Evolution RADIO LIVE TEST124 - receiver trial"
    )


def data_members():
    result = []
    for src in SOURCE.rglob("*"):
        rel = src.relative_to(SOURCE).as_posix()
        # Syntax preflight generates local bytecode; never package it.
        if "__pycache__" in src.parts or src.suffix in (".pyc", ".pyo"):
            continue
        if src.name in BLOCKED_GRAPHICS:
            continue
        if src.suffix == ".po":
            continue
        # Preserve the existing on-demand locale delivery contract.
        if src.suffix == ".mo" and rel.startswith(PLUGIN + "/locale/"):
            if rel.split("/locale/", 1)[1].split("/", 1)[0] != "en":
                continue
        result.append((src, rel))
    return sorted(result, key=lambda pair: pair[1])


def write_tar(destination, members, replacements=None):
    replacements = replacements or {}
    with destination.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w", format=tarfile.GNU_FORMAT) as archive:
                for source, rel in members:
                    name = "./" + rel
                    info = archive.gettarinfo(str(source), arcname=name)
                    info.uid = info.gid = info.mtime = 0
                    info.uname = info.gname = ""
                    if source.is_symlink():
                        # Retain the source's symlink; never follow to host files.
                        archive.addfile(info)
                    elif source.is_file():
                        payload = replacements.get(rel)
                        if payload is None:
                            payload = source.read_bytes()
                        info.size = len(payload)
                        archive.addfile(info, io.BytesIO(payload))
                    else:
                        archive.addfile(info)


def inspect(ipk):
    names = subprocess.check_output(["ar", "t", str(ipk)], text=True).splitlines()
    if names != ["debian-binary", "control.tar.gz", "data.tar.gz"]:
        raise RuntimeError("Invalid IPK ar member layout: " + repr(names))
    control_bytes = subprocess.check_output(["ar", "p", str(ipk), "control.tar.gz"])
    with tarfile.open(fileobj=io.BytesIO(control_bytes), mode="r:gz") as tar:
        control = tar.extractfile("./control").read().decode("utf-8")
        assert "Package: " + PACKAGE_ID + "\n" in control
        assert "Version: " + PACKAGE_VERSION + "\n" in control
        for file in ("preinst", "postinst", "postrm", "conffiles"):
            assert "./" + file in tar.getnames(), "Missing installer: " + file
    payload = subprocess.check_output(["ar", "p", str(ipk), "data.tar.gz"])
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tar:
        files = set(item.name.removeprefix("./") for item in tar.getmembers())
        if REQUIRED - files:
            raise RuntimeError("Incomplete RADIO LIVE files: " + repr(REQUIRED - files))
        if any(Path(name).name in BLOCKED_GRAPHICS for name in files):
            raise RuntimeError("Unapproved menu graphic found inside test IPK")
        source = tar.extractfile("./" + VERSION_REL).read().decode("utf-8").strip()
        assert source == RUNTIME_VERSION, "Runtime version mismatch"
        manifest = {"package": PACKAGE_ID, "package_version": PACKAGE_VERSION,
                    "runtime_version": source, "file_count": len(files),
                    "bridge_files": sorted(REQUIRED), "release_type": "TEST-only"}
    return manifest


def main():
    control = check_sources()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUT_DIR / (PKG_NAME + "_" + RUNTIME_VERSION + "_all.ipk")
    with tempfile.TemporaryDirectory(prefix="warder-radio-live-test-") as directory:
        temp = Path(directory)
        db = temp / "debian-binary"
        db.write_bytes(b"2.0\n")
        controls = [(p, p.name) for p in (CONTROL / "control", CONTROL / "conffiles",
                                          CONTROL / "preinst", CONTROL / "postinst",
                                          CONTROL / "postrm")]
        write_tar(temp / "control.tar.gz", controls, {"control": control.encode("utf-8")})
        write_tar(temp / "data.tar.gz", data_members(), {
            VERSION_REL: (RUNTIME_VERSION + "\n").encode("utf-8")
        })
        subprocess.run(["ar", "rcs", str(destination), "debian-binary",
                        "control.tar.gz", "data.tar.gz"],
                       cwd=temp, check=True)
    summary = inspect(destination)
    summary["size_bytes"] = destination.stat().st_size
    summary["sha256"] = hashlib.sha256(destination.read_bytes()).hexdigest()
    (OUT_DIR / (destination.name + ".sha256")).write_text(
        summary["sha256"] + "  " + destination.name + "\n", encoding="utf-8")
    (OUT_DIR / "radio-live-test128-manifest.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
