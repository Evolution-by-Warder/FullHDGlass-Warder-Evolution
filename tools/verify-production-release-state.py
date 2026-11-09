#!/usr/bin/env python3
"""Fail-closed production release consistency check.

A published release is complete only when main's version, metadata, production
feed, checked-in IPK, SHA256 and GitHub Release asset all agree.
This guard intentionally NEVER repairs or publishes an incomplete release.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = os.environ.get("GITHUB_REPOSITORY", "Evolution-by-Warder/FullHDGlass-Warder-Evolution")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def load_json(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "warder-release-integrity"}
    if TOKEN:
        headers["Authorization"] = "Bearer " + TOKEN
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=25) as response:
        return json.load(response)

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def check():
    version = (ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/version").read_text().strip()
    metadata = (ROOT / "source/control/control").read_text()
    require("Version: " + version + "-1" in metadata.splitlines(), "IPK control version differs from runtime version")
    feed = json.loads((ROOT / "update-production.json").read_text(encoding="utf-8"))
    require(feed.get("version") == version, "Production feed is behind source: " + str(feed.get("version")) + " vs " + version)
    name = "enigma2-plugin-skins-fullhdglass_" + version + "_all.ipk"
    package = ROOT / "packages" / name
    require(package.is_file(), "Official IPK missing from main: " + name)
    digest = hashlib.sha256(package.read_bytes()).hexdigest()
    require(feed.get("sha256") == digest, "Production feed checksum differs from official IPK")
    expected_url = "https://raw.githubusercontent.com/" + REPO + "/main/packages/" + name
    require(feed.get("package_url") == expected_url, "Production feed URL is incorrect")
    checksum_file = package.with_name(name + ".sha256")
    require(checksum_file.is_file(), "Release checksum file is missing")
    require(digest in checksum_file.read_text(), "Checksum file does not match published IPK")
    release = load_json("https://api.github.com/repos/" + REPO + "/releases/tags/v" + version)
    require(not release.get("draft") and not release.get("prerelease"), "Official release is draft/prerelease")
    asset = next((a for a in release.get("assets", []) if a.get("name") == name), None)
    require(asset and asset.get("size") == package.stat().st_size, "GitHub Release asset missing or differs in size")
    check_asset = next((a for a in release.get("assets", []) if a.get("name") == name + ".sha256"), None)
    require(check_asset is not None, "GitHub Release checksum asset is missing")
    print("PASS: source, production feed, IPK bytes, SHA256, official tag and Release assets:", version)

if __name__ == "__main__":
    try:
        check()
    except (AssertionError, OSError, ValueError, urllib.error.URLError) as exc:
        print("RELEASE INCOMPLETE:", exc, file=sys.stderr)
        sys.exit(1)
