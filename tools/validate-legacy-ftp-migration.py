#!/usr/bin/env python3
"""Validate the one-way legacy HDGlass FTP -> Warder migration ledger."""
from pathlib import Path
import csv, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "assets/warder/legacy-ftp-migration.tsv"
CATALOG = ROOT / "assets/catalog.json"
MANIFEST = ROOT / "assets/warder/downloads.json"

errors = []
with LEDGER.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
assets = manifest.get("assets", {})
families = {x["id"]: x for x in catalog.get("families", [])}

required = {"legacy_path","logical_service","runtime_key","warder_path","legacy_sha256","current_sha256","migration_state","runtime_route"}
if not rows or not required.issubset(rows[0]):
    errors.append("migration ledger schema is incomplete")

seen_legacy = set()
seen_keys = set()
for row in rows:
    legacy = row["legacy_path"]
    key = row["runtime_key"]
    route = row["runtime_route"]
    state = row["migration_state"]
    if legacy in seen_legacy:
        errors.append("duplicate legacy path: %s" % legacy)
    seen_legacy.add(legacy)
    if route == "LEGACY_FTP":
        errors.append("forbidden LEGACY_FTP runtime route: %s" % legacy)
    if route == "WARDER_MANIFEST":
        if not key:
            errors.append("missing runtime key: %s" % legacy)
            continue
        if key in seen_keys:
            errors.append("duplicate runtime key in migration ledger: %s" % key)
        seen_keys.add(key)
        if key not in assets:
            errors.append("Warder manifest missing key %s" % key)
        elif str(assets[key].get("sha256", "")).lower() != row["current_sha256"]:
            errors.append("ledger/manifest SHA256 mismatch for %s" % key)
        if key not in families or families[key].get("status") not in ("available","internal-only"):
            errors.append("catalog does not expose migrated key %s" % key)
        sha = row["current_sha256"]
        if not re.fullmatch(r"[0-9a-f]{64}", sha or ""):
            errors.append("invalid current SHA256 for %s" % legacy)
    elif route == "NOT_EXPOSED":
        if state != "SOURCE_PRESERVED_TARGET_MISSING":
            errors.append("NOT_EXPOSED state mismatch: %s" % legacy)
        if key in assets:
            errors.append("NOT_EXPOSED key unexpectedly published: %s" % key)
    elif route != "ARCHIVE_ONLY":
        errors.append("unknown runtime route %s for %s" % (route, legacy))

for key, asset in assets.items():
    urls = asset.get("parts") or [asset.get("url","")]
    for url in urls:
        if url and not url.startswith("https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/"):
            errors.append("non-Warder asset URL for %s" % key)

# Runtime architecture helper invariant: never synthesize an unpublished SH4 helper key.
plugin = (ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py").read_text(encoding="utf-8")
if '"sh4":"s"' in plugin or "7zip-s" in assets:
    errors.append("unpublished SH4 7zip helper route is present")

if errors:
    for e in errors:
        print("ERROR:", e)
    sys.exit(1)
print("PASS legacy FTP migration ledger: %d rows, %d Warder-routed, %d not exposed, %d archive-only" % (
    len(rows),
    sum(r["runtime_route"] == "WARDER_MANIFEST" for r in rows),
    sum(r["runtime_route"] == "NOT_EXPOSED" for r in rows),
    sum(r["runtime_route"] == "ARCHIVE_ONLY" for r in rows),
))
