#!/usr/bin/env python3
"""Validate the one-way legacy HDGlass FTP -> Warder migration ledger."""
from pathlib import Path
import csv, json, re, sys
from urllib.parse import urlsplit

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

# Explicit Warder publication roots. The PiconHub allowance is deliberately
# limited to the pinned TEST202 auxiliary candidate archive set.
FULLHD_ROOT = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/"
PICONHUB_REPO = "Evolution-by-Warder/PiconHub-Warder-Evolution"
PICONHUB_COMMIT = "db5eec9f1cdb7a4d587cb1bcdeebc6b3f0d51819"
PICONHUB_CANDIDATE_PATH = "reports/warder-master-production/auxiliary-hybrid-runtime-candidate-2026-10-07"
PICONHUB_ARCHIVE_PATH = PICONHUB_CANDIDATE_PATH + "/archives"
PICONHUB_MANIFEST_URL = "https://raw.githubusercontent.com/%s/%s/%s/candidate-downloads.json" % (PICONHUB_REPO, PICONHUB_COMMIT, PICONHUB_CANDIDATE_PATH)
PICONHUB_ROOT = "https://raw.githubusercontent.com/%s/%s/%s/" % (PICONHUB_REPO, PICONHUB_COMMIT, PICONHUB_ARCHIVE_PATH)
PICONHUB_ASSETS = {
    "piconProv-legacy-t": "provider-transparent-legacy-fallback.zip",
    "piconProv-warder-safe-b": "provider-black-warder-safe-220x132.zip",
    "piconProv-warder-safe-t": "provider-transparent-warder-safe-220x132.zip",
    "piconProv-warder-safe-w": "provider-white-warder-safe-220x132.zip",
    "piconSat-legacy-t": "satellite-transparent-legacy-fallback.zip",
    "piconSat-warder-safe-b": "satellite-black-warder-safe-220x132.zip",
    "piconSat-warder-safe-t": "satellite-transparent-warder-safe-220x132.zip",
    "piconSat-warder-safe-w": "satellite-white-warder-safe-220x132.zip",
}


def _safe_raw_github_url(url):
    """Reject URL spellings that can obscure host or path-boundary checks."""
    if not isinstance(url, str):
        return None
    try:
        parsed = urlsplit(url)
    except Exception:
        return None
    path = parsed.path
    if (parsed.scheme != "https" or parsed.netloc != "raw.githubusercontent.com"
            or parsed.hostname != "raw.githubusercontent.com"
            or parsed.username or parsed.password or parsed.port
            or parsed.query or parsed.fragment or "%" in path or "\\\\" in path
            or not path.startswith("/") or "//" in path):
        return None
    segments = path.split("/")
    if any(segment in (".", "..") for segment in segments):
        return None
    if not re.fullmatch(r"/[A-Za-z0-9._/-]+", path):
        return None
    return parsed


def _publication_url_allowed(url, key, asset, publication):
    """Check a runtime URL against its one explicit Warder publication source."""
    parsed = _safe_raw_github_url(url)
    if parsed is None:
        return False
    source_id = asset.get("publication_source_id")
    if source_id == "piconhub-aux-candidate":
        if not isinstance(publication, dict):
            return False
        if (publication.get("candidate_source_id") != "piconhub-aux-candidate"
                or publication.get("candidate_commit") != PICONHUB_COMMIT
                or publication.get("candidate_manifest_url") != PICONHUB_MANIFEST_URL):
            return False
        expected_name = PICONHUB_ASSETS.get(key)
        if not expected_name or asset.get("filename") != expected_name:
            return False
        return url == PICONHUB_ROOT + expected_name
    if source_id not in (None, "fullhd-production"):
        return False
    # The production source is the FullHDGlass main publication root only.
    return url.startswith(FULLHD_ROOT) and len(url) > len(FULLHD_ROOT)


def _publication_url_policy_regressions():
    """Exercise allow and deny cases for both explicit source roots."""
    publication = {
        "candidate_source_id": "piconhub-aux-candidate",
        "candidate_commit": PICONHUB_COMMIT,
        "candidate_manifest_url": PICONHUB_MANIFEST_URL,
    }
    sample_key = "piconProv-warder-safe-t"
    sample_asset = {
        "publication_source_id": "piconhub-aux-candidate",
        "filename": PICONHUB_ASSETS[sample_key],
    }
    valid_candidate = PICONHUB_ROOT + PICONHUB_ASSETS[sample_key]
    valid_production = FULLHD_ROOT + "picons/providers/black/piconProv.zip"
    production_asset = {"publication_source_id": "fullhd-production"}
    checks = (
        _publication_url_allowed(valid_candidate, sample_key, sample_asset, publication),
        _publication_url_allowed(valid_production, "piconProv-b", production_asset, publication),
        not _publication_url_allowed(valid_candidate.replace(PICONHUB_COMMIT, "a" * 40), sample_key, sample_asset, publication),
        not _publication_url_allowed(PICONHUB_ROOT + "other/" + PICONHUB_ASSETS[sample_key], sample_key, sample_asset, publication),
        not _publication_url_allowed(valid_candidate.replace(PICONHUB_REPO, "someone/else"), sample_key, sample_asset, publication),
        not _publication_url_allowed(valid_candidate.replace("https://", "http://"), sample_key, sample_asset, publication),
        not _publication_url_allowed(valid_candidate.replace(PICONHUB_COMMIT, "warder-modernization-work"), sample_key, sample_asset, publication),
        not _publication_url_allowed(PICONHUB_ROOT + "../escape.zip", sample_key, sample_asset, publication),
        not _publication_url_allowed(valid_candidate, sample_key, sample_asset, {"candidate_source_id": "piconhub-aux-candidate", "candidate_commit": PICONHUB_COMMIT, "candidate_manifest_url": PICONHUB_MANIFEST_URL + ".wrong"}),
        not _publication_url_allowed(valid_candidate, sample_key, {"publication_source_id": "fullhd-production", "filename": sample_asset["filename"]}, publication),
    )
    return all(checks)


publication = manifest.get("auxiliary_hybrid", {})
if publication:
    if not _publication_url_policy_regressions():
        errors.append("publication URL policy regression failed")
    expected_manifest_url = PICONHUB_MANIFEST_URL
    if (publication.get("candidate_source_id") != "piconhub-aux-candidate"
            or publication.get("candidate_commit") != PICONHUB_COMMIT
            or publication.get("candidate_manifest_url") != expected_manifest_url):
        errors.append("PiconHub auxiliary publication descriptor is not the approved pinned source")

for key, asset in assets.items():
    urls = asset.get("parts") or [asset.get("url", "")]
    for url in urls:
        if url and not _publication_url_allowed(url, key, asset, publication):
            errors.append("asset URL outside explicit Warder publication policy for %s" % key)

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
