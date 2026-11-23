#!/usr/bin/env python3
"""Fail-closed cleanup for old FullHDGlass IPK copies in the main source tree.

GitHub Releases remain immutable; package file removal never deletes a tag,
Release, artwork, user data or archive in another directory. The old 1.0.18
migration identity and 1.0.72 legacy TEST-branch target are exceptions.
"""
import argparse
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parents[1]
PREFIX = "enigma2-plugin-skins-fullhdglass_"
PAIR = re.compile(r"^enigma2-plugin-skins-fullhdglass_(\d+\.\d+\.\d+)_all\.ipk$")
MAX_STABLE = 4
PINNED_LEGACY_TEST = {"1.0.72"}
BOOTSTRAP = "enigma2-skin-fullhdglass-warder-evolution_1.0.18_all.ipk"


def version_key(version):
    return tuple(int(part) for part in version.split("."))


def plan(root):
    root = Path(root)
    packages = root / "packages"
    if not packages.is_dir():
        raise ValueError("packages directory was not checked out")
    feed = json.loads((root / "update-production.json").read_text(encoding="utf-8"))
    test_feed = json.loads((root / "update-test.json").read_text(encoding="utf-8"))
    bootstrap_feed = json.loads((root / "update.json").read_text(encoding="utf-8"))
    current = (root / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/version").read_text().strip()
    if feed.get("version") != current or test_feed.get("version") != current:
        raise ValueError("stable/test feeds do not agree with current version")
    if bootstrap_feed.get("version") != "1.0.18":
        raise ValueError("old installation bootstrap changed; unsafe to prune")
    if not bootstrap_feed.get("package_url", "").endswith("/" + BOOTSTRAP):
        raise ValueError("legacy bootstrap package URL changed")
    if not (packages / BOOTSTRAP).is_file() or not (packages / (BOOTSTRAP + ".sha256")).is_file():
        raise ValueError("legacy 1.0.18 bootstrap was lost")
    records = {}
    for package in packages.glob("*.ipk"):
        match = PAIR.fullmatch(package.name)
        if not match:
            if package.name != BOOTSTRAP:
                raise ValueError("unexpected package identity: " + package.name)
            continue
        version = match.group(1)
        sha = packages / (package.name + ".sha256")
        if not sha.is_file() or not sha.read_text(encoding="utf-8").strip():
            raise ValueError("missing checksum: " + sha.name)
        records[version] = (package, sha)
    for checksum in packages.glob("*.ipk.sha256"):
        if not (packages / checksum.name.removesuffix(".sha256")).is_file():
            raise ValueError("orphan checksum: " + checksum.name)
    ordered = sorted(records, key=version_key, reverse=True)
    if len(ordered) < MAX_STABLE or ordered[0] != current:
        raise ValueError("latest four stable versions unavailable")
    kept_stable = ordered[:MAX_STABLE]
    protected = set(kept_stable) | PINNED_LEGACY_TEST
    for field in (feed, test_feed, bootstrap_feed):
        url = field.get("package_url", "")
        for version, (package, unused_checksum) in records.items():
            if url.endswith("/" + package.name):
                protected.add(version)
    if feed["package_url"] != test_feed["package_url"] or feed["sha256"] != test_feed["sha256"]:
        raise ValueError("test feeder cannot safely follow current stable")
    removed = [path for version in ordered if version not in protected for path in records[version]]
    return {"stable": kept_stable, "exceptions": sorted(protected - set(kept_stable)),
            "remove": removed, "retained": sorted(protected, key=version_key, reverse=True)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=HERE)
    parser.add_argument("--apply", action="store_true", help="Delete only the reviewed obsolete pairs")
    args = parser.parse_args()
    result = plan(args.root)
    total = sum(p.stat().st_size for p in result["remove"])
    print("FOUR_STABLE", result["stable"], "EXCEPTIONS", result["exceptions"],
          "OLD_FILES", len(result["remove"]), "BYTES", total)
    if args.apply:
        for path in result["remove"]:
            path.unlink()
        print("Removed obsolete IPK copies from working tree; Git history/Release unchanged.")


if __name__ == "__main__":
    main()
