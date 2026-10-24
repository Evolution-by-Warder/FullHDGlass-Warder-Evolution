#!/usr/bin/env python3
"""Publish a verified two-step native skin-package migration."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("migration_publisher", ROOT / "tools/publish-settings-update.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
NEW = "enigma2-plugin-skins-fullhdglass-warder-evolution"
LEGACY = "enigma2-skin-fullhdglass-warder-evolution"


def read_build(folder, version, prefix, revision):
    path = folder / (prefix + "_" + version + "_all.ipk")
    info = json.loads((folder / "settings-ui-build.json").read_text())
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if (info["version"], info["package"], info["source_commit"], info["bytes"], info["sha256"]) != (version, path.name, revision, len(data), digest):
        raise ValueError("Migration build identity mismatch")
    if not 0 < len(data) < 16 * 1024 * 1024:
        raise ValueError("Migration package exceeds size budget")
    return path, info, data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    approval = json.loads((ROOT / "docs/PRODUCTION-APPROVAL.json").read_text())
    client = p.GitHub(os.environ["GH_TOKEN"])
    builds = [
        read_build(ROOT / "packages/bridge", approval["transition_version"], LEGACY, args.revision),
        read_build(ROOT / "packages/test", approval["production_version"], NEW, args.revision),
    ]
    releases = []
    for path, info, raw in builds:
        release = client.request("GET", "/releases/tags/v" + info["version"])
        asset = next(a for a in release["assets"] if a["name"] == path.name)
        if release["draft"] or release["target_commitish"] != args.revision:
            raise ValueError("Migration release source mismatch")
        if asset["size"] != len(raw) or asset["digest"] != "sha256:" + info["sha256"]:
            raise ValueError("Migration release asset mismatch")
        p.verify_public(client, asset["browser_download_url"], len(raw), info["sha256"])
        releases.append(release)
    for entry in approval["preview_assets"].values():
        p.verify_public(client, entry["url"], entry["size"], entry["sha256"])
    if p.head(client, "main") != approval["expected_main_sha"] or p.head(client, p.WORK) != args.revision:
        raise ValueError("Source advanced before migration publication")
    files = {}
    for path, info, raw in builds:
        files["packages/" + path.name] = raw
        files["packages/" + path.name + ".sha256"] = (info["sha256"] + "  " + path.name + "\n").encode()
    staged = p.commit(client, args.revision, files, "Stage verified bridge and native FullHDGlass packages")
    p.advance(client, "main", approval["expected_main_sha"], staged)
    for path, info, raw in builds:
        p.verify_public(client, p.RAW + path.name, len(raw), info["sha256"])
    if p.head(client, p.WORK) != args.revision:
        raise ValueError("Source advanced; migration feeds remain unchanged")
    def feed(build, notes):
        path, info, raw = build
        return {"version": info["version"], "package_url": p.RAW + path.name,
                "sha256": info["sha256"], "changelog": notes}
    bridge = feed(builds[0], "Migračná aktualizácia pripraví zachovanie nastavení pri premenovaní balíka. Po reštarte GUI otvor konfiguráciu a potvrď následnú aktualizáciu 1.0.19 pre zobrazenie medzi nainštalovanými Balíčkami vzhľadu.")
    native = feed(builds[1], "FullHDGlass Warder Evolution je zaradený medzi nainštalované Balíčky vzhľadu. Vnútorné priečinky, schválená grafika a uložené nastavenia zostávajú zachované.")
    legacy_data = p.encoded(bridge)
    inventory = json.loads(p.content(client, "design/settings-ui-inventory.json", "main"))
    inventory.update(current_feed_version=bridge["version"], production_feed_version=native["version"])
    inventory["feeds_sha256"] = {name: hashlib.sha256(legacy_data).hexdigest() for name in ("update.json", "update-test.json")}
    path, info, raw = builds[1]
    record = {
        "schema": 1, "product": approval["product"], "status": "production-approved",
        "approved_on": approval["approved_on"], "approval": approval["authorization"],
        "source_branch": p.WORK, "source_commit": args.revision, "package_id": NEW,
        "release": dict(native, tag="v" + native["version"], bytes=len(raw),
                        url=next(a["browser_download_url"] for a in releases[1]["assets"] if a["name"] == path.name)),
        "transition": dict(bridge, package_id="enigma2-skin-fullhdglass17", bytes=builds[0][1]["bytes"]),
        "preview_assets": approval["preview_assets"],
        "validation": {"workflow_run": int(os.environ["GITHUB_RUN_ID"]),
                       "build_payloads_and_public_bytes": "verified",
                       "receiver_validation": "No physical receiver test of the package-name migration is claimed."}
    }
    changes = {"update.json": legacy_data, "update-test.json": legacy_data,
               "update-production.json": p.encoded(native),
               "design/settings-ui-inventory.json": p.encoded(inventory),
               "docs/PRODUCTION.json": p.encoded(record),
               "docs/LIVE-UPDATE-STATE.json": p.encoded(dict(native, bytes=len(raw), source_commit=args.revision,
                   production_status="production-approved", production_tag="v"+native["version"],
                   legacy_bridge_version=bridge["version"]))}
    activated = p.commit(client, staged, changes, "Activate safe FullHDGlass bridge 1.0.18 and native skins package 1.0.19")
    p.advance(client, "main", staged, activated)
    p.advance(client, p.WORK, args.revision, activated)
    for index, release in enumerate(releases):
        result = client.request("PATCH", "/releases/" + str(release["id"]),
                                {"draft": False, "prerelease": False, "make_latest": "true" if index else "false"})
        if result["draft"] or result["prerelease"]:
            raise ValueError("Migration production promotion failed")
    print("Verified production packages: bridge", bridge["version"], "native", native["version"])


if __name__ == "__main__":
    main()

