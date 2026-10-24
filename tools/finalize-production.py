#!/usr/bin/env python3
"""Record and promote a verified stable skin after both updater feeds advance."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("settings_publisher", ROOT / "tools/publish-settings-update.py")
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--build-info", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    approval = json.loads((ROOT / "docs/PRODUCTION-APPROVAL.json").read_text())
    info = json.loads(args.build_info.read_text())
    version = info["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version) or approval["production_version"] != version:
        raise ValueError("Stable production approval does not match build")
    raw = args.package.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if info["source_commit"] != args.revision or info["sha256"] != digest or info["bytes"] != len(raw):
        raise ValueError("Build identity mismatch")
    name = "enigma2-skin-fullhdglass-warder-evolution_" + version + "_all.ipk"
    if args.package.name != name or len(raw) >= 16 * 1024 * 1024:
        raise ValueError("Package identity or size mismatch")
    client = publisher.GitHub(os.environ["GH_TOKEN"])
    head = publisher.head(client, "main")
    if publisher.head(client, publisher.WORK) != head:
        raise ValueError("Branches differ after updater publication")
    for branch, path in (("main", "update.json"), (publisher.WORK, "update-test.json")):
        feed = json.loads(publisher.content(client, path, branch))
        if (feed["version"], feed["sha256"], feed["package_url"]) != (version, digest, publisher.RAW + name):
            raise ValueError("Updater does not offer verified stable package")
    tag = "v" + version
    release = client.request("GET", "/releases/tags/" + tag)
    if release["draft"] or release["target_commitish"] != args.revision:
        raise ValueError("Release source mismatch")
    tag_ref = client.request("GET", "/git/ref/tags/" + tag)["object"]
    if tag_ref["type"] == "tag":
        tag_ref = client.request("GET", "/git/tags/" + tag_ref["sha"])["object"]
    if tag_ref["type"] != "commit" or tag_ref["sha"] != args.revision:
        raise ValueError("Release tag source mismatch")
    asset = next(item for item in release["assets"] if item["name"] == name)
    if asset["size"] != len(raw) or asset["digest"] != "sha256:" + digest:
        raise ValueError("Release asset mismatch")
    publisher.verify_public(client, publisher.RAW + name, len(raw), digest)
    publisher.verify_public(client, asset["browser_download_url"], len(raw), digest)
    assets = approval["preview_assets"]
    for entry in assets.values():
        publisher.verify_public(client, entry["url"], entry["size"], entry["sha256"])
    record = {
        "schema": 1, "product": approval["product"], "status": "production-approved",
        "approved_on": approval["approved_on"], "approval": approval["authorization"],
        "source_branch": publisher.WORK, "source_commit": args.revision,
        "release": {"version": version, "tag": tag, "url": asset["browser_download_url"],
                    "package_url": publisher.RAW + name, "sha256": digest, "bytes": len(raw)},
        "preview_assets": assets, "baseline": approval["baseline"],
        "validation": {"workflow_run": int(os.environ["GITHUB_RUN_ID"]),
                       "automated_build_and_payload_checks": "passed",
                       "public_package_and_previews": "verified",
                       "owner_acceptance": "Current skin approved for production on 24 October 2026.",
                       "receiver_validation": "No new exhaustive physical receiver test is claimed."}
    }
    previous = json.loads(publisher.content(client, "docs/LIVE-UPDATE-STATE.json", "main"))
    previous.update(production_status="production-approved", production_tag=tag, approved_on=approval["approved_on"])
    commit = publisher.commit(client, head, {
        "docs/PRODUCTION.json": publisher.encoded(record),
        "docs/LIVE-UPDATE-STATE.json": publisher.encoded(previous)
    }, "Record verified FullHDGlass " + version + " production release")
    publisher.advance(client, "main", head, commit)
    publisher.advance(client, publisher.WORK, head, commit)
    result = client.request("PATCH", "/releases/" + str(release["id"]),
                            {"draft": False, "prerelease": False, "make_latest": "true"})
    if result["draft"] or result["prerelease"]:
        raise ValueError("Stable release promotion failed")
    print("Verified production release:", version, len(raw), digest, result["html_url"])


if __name__ == "__main__":
    main()

