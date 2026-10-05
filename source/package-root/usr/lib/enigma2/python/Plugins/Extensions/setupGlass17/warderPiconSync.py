# -*- coding: utf-8 -*-
"""FullHDGlass17 Warder Evolution - receiver driven picon synchronisation.

Pure planning helpers live here so the Enigma2 GUI can stay small.  No network
or GUI side effects are performed by this module.
"""
from __future__ import absolute_import

import os
import re
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

ENIGMA2_DIR = "/etc/enigma2"
# Explicit two-phase cutover switch. Publication evidence and this runtime switch
# are reviewed separately; never infer readiness merely from network reachability.
RUNTIME_PUBLICATION_ENABLED = True
RUNTIME_MANIFEST_URL = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/manifest.json"
_BOUQUET_RE = re.compile(r'FROM BOUQUET "([^"]+)"', re.I)
_HEX = re.compile(r"^[0-9A-Fa-f]+$")


def normalize_service_reference(reference):
    """Return the canonical Enigma2 picon filename stem for a service ref."""
    if reference is None:
        return ""
    ref = str(reference).strip()
    if ref.startswith("#SERVICE"):
        ref = ref.split(None, 1)[1].strip() if " " in ref else ""
    ref = ref.split("::", 1)[0].strip()
    if ":" in ref:
        fields = ref.split(":")
    else:
        fields = ref.split("_")
    if len(fields) < 10:
        return ""
    fields = fields[:10]
    if not all(_HEX.match(x or "0") for x in fields):
        return ""
    return "_".join((x or "0").upper() for x in fields)


def namespace_to_orbital_position(namespace):
    """Map DVB-S namespace to PiconHub folder form such as 23.5e or 0.8w."""
    try:
        value = int(str(namespace), 16) if not isinstance(namespace, int) else namespace
    except (TypeError, ValueError):
        return None
    orbital = (value >> 16) & 0xFFFF
    if orbital == 0 or orbital == 0xFFFF:
        return None
    if orbital > 1800:
        orbital = 3600 - orbital
        suffix = "w"
    else:
        suffix = "e"
    return "%d.%d%s" % (orbital // 10, orbital % 10, suffix)


def position_token(label):
    """Normalize a SATLIST/user label to the planner token (23.5e, 0.8w, dtt)."""
    text = str(label or "").strip()
    if text.upper().startswith("DVB-T"):
        return "dtt"
    match = re.search(r"\(([0-9]+(?:\.[0-9]+)?)([EW])\)", text, re.I)
    if match:
        return match.group(1).lower() + match.group(2).lower()
    if re.match(r"^[0-9]+(?:\.[0-9]+)?[ew]$", text, re.I):
        return text.lower()
    return text.lower()


def service_orbital_position(reference):
    stem = normalize_service_reference(reference)
    if not stem:
        return None
    fields = stem.split("_")
    return namespace_to_orbital_position(fields[6])


def _read_lines(path):
    try:
        with open(path, "r") as handle:
            return handle.readlines()
    except (IOError, OSError):
        return []


def bouquet_files(enigma2_dir=ENIGMA2_DIR, root_name="bouquets.tv"):
    """Return bouquet files referenced by bouquets.tv, preserving user order."""
    result = []
    seen = set()
    for line in _read_lines(os.path.join(enigma2_dir, root_name)):
        match = _BOUQUET_RE.search(line)
        if not match:
            continue
        name = os.path.basename(match.group(1))
        if name in seen:
            continue
        seen.add(name)
        result.append(os.path.join(enigma2_dir, name))
    return result


def bouquet_services(enigma2_dir=ENIGMA2_DIR, include_radio=False):
    """Read exact playable service references from receiver bouquet files."""
    roots = ["bouquets.tv"]
    if include_radio:
        roots.append("bouquets.radio")
    refs = []
    seen = set()
    for root in roots:
        for path in bouquet_files(enigma2_dir, root):
            for line in _read_lines(path):
                if not line.startswith("#SERVICE"):
                    continue
                raw = line[len("#SERVICE"):].strip()
                if "FROM BOUQUET" in raw.upper():
                    continue
                stem = normalize_service_reference(raw)
                if not stem or stem in seen:
                    continue
                seen.add(stem)
                refs.append(stem)
    return refs


def build_sync_request(enigma2_dir=ENIGMA2_DIR, selected_positions=None,
                       style="transparent", resolution="220x132",
                       include_radio=False):
    """Build a deterministic receiver-driven request; no provider guessing."""
    selected = set(x.lower() for x in (selected_positions or []) if x)
    services = []
    for stem in bouquet_services(enigma2_dir, include_radio):
        position = service_orbital_position(stem.replace("_", ":"))
        if selected and (not position or position.lower() not in selected):
            continue
        services.append({"service_reference": stem, "position": position})
    return {
        "mode": "sync-tv-lists",
        "style": style,
        "resolution": resolution,
        "services": services,
    }


UPDATE_MODE_SYNC_TV = "sync-tv-lists"
UPDATE_MODE_FULL = "full"
DEFAULT_UPDATE_MODE = UPDATE_MODE_SYNC_TV
DEFAULT_STYLE = "transparent"
DEFAULT_RESOLUTION = "220x132"

UPDATE_MODES = (
    (UPDATE_MODE_SYNC_TV, "Synchronize with TV lists"),
    (UPDATE_MODE_FULL, "FULL"),
)
STYLES = (
    ("transparent", "Transparent"),
    ("black", "Black"),
    ("white", "White"),
)
RESOLUTIONS = (
    ("220x132", "220 x 132"),
)


def default_preferences(destination="/media/hdd/picon"):
    return {
        "positions": [],
        "resolution": DEFAULT_RESOLUTION,
        "style": DEFAULT_STYLE,
        "destination": destination,
        "update_mode": DEFAULT_UPDATE_MODE,
        "prepared": False,
    }


def set_preference(preferences, key, value):
    """Return a copied preference state and mark it as a prepared action."""
    if key not in ("positions", "resolution", "style", "destination", "update_mode"):
        raise KeyError(key)
    result = dict(preferences)
    result[key] = value
    result["prepared"] = True
    return result


def has_executable_action(preferences, ordinary_selected=False):
    """Mirror FullHDGlass blue-button semantics for the assimilated planner."""
    return bool(ordinary_selected or preferences.get("prepared", False))


PUBLICATION_LOCKED = "publication-locked"
READY = "ready"


# SATLIST identity must stay separate from orbital filtering. Provider selectors can
# share one orbital position, while nearby legacy selectors may have distinct IDs.
_SPECIAL_SELECTOR_LABELS = {
    "(0.8W) Freesat": "FREESAT",
    "(0.8W) Digi / Telly": "DIGI_TELLY",
    "(0.8W) Digi/Telly": "DIGI_TELLY",
    "(16.0E) Antiksat": "ANTIKSAT",
    "(23.5E) Skylink": "SKYLINK",
    "DVB-T sk/cz": "DVB-T-SK-CZ",
}
_ORBITAL_SELECTOR_IDS = {
    "45.0w":"450W","30.0w":"300W","27.5w":"275W","24.5w":"248W","22.0w":"220W",
    "15.0w":"150W","14.0w":"140W","12.5w":"125W","11.0w":"110W","8.0w":"80W",
    "7.0w":"70W","5.0w":"50W","4.0w":"40W","1.0w":"10W","0.8w":"08W",
    "1.9e":"19E","3.0e":"30E","3.1e":"31E","4.8e":"48E_A","4.9e":"48E_B",
    "7.0e":"70E","9.0e":"90E","10.0e":"100E","13.0e":"130E","16.0e":"160E",
    "19.2e":"192E","21.5e":"216E","23.5e":"235E","26.0e":"260E","28.2e":"282E",
    "30.5e":"305E","31.5e":"315E","33.0e":"330E","36.0e":"360E","39.0e":"390E",
    "42.0e":"420E","45.0e":"450E","46.0e":"460E","51.5e":"515E","52.0e":"520E",
    "52.5e":"525E","53.0e":"530E","54.9e":"549E","56.0e":"560E","62.0e":"620E",
    "66.0e":"660E","68.5e":"685E","70.5e":"705E","74.9e":"749E","75.0e":"750E",
    "85.0e":"850E","85.1e":"851E",
}

def selector_id(label):
    text = str(label or "").strip()
    if text in _SPECIAL_SELECTOR_LABELS:
        return _SPECIAL_SELECTOR_LABELS[text]
    return _ORBITAL_SELECTOR_IDS.get(position_token(text))


def selected_selector_ids(labels):
    result = []
    seen = set()
    for label in labels or []:
        sid = selector_id(label)
        if sid and sid not in seen:
            seen.add(sid)
            result.append(sid)
    return result


def family_for_style(style):
    return {
        "transparent": "channel-transparent",
        "black": "channel-black",
        "white": "channel-white",
    }.get(style)


def select_manifest_packages(document, preferences):
    """Select deterministic packages; never substitute another selector/family."""
    errors = validate_publication_manifest(document)
    if errors:
        return {"state": "invalid-manifest", "packages": [], "errors": errors}
    prefs = dict(default_preferences())
    prefs.update(preferences or {})
    family = family_for_style(prefs.get("style"))
    if not family:
        return {"state": "unsupported-style", "packages": [], "errors": ["unsupported style"]}
    wanted = selected_selector_ids(prefs.get("positions"))
    resolution = prefs.get("resolution", DEFAULT_RESOLUTION)
    packages = [p for p in document.get("packages", [])
                if p.get("family") == family and p.get("resolution") == resolution]
    if wanted:
        wanted_set = set(wanted)
        packages = [p for p in packages if p.get("selector_id") in wanted_set]
        available = set(p.get("selector_id") for p in packages)
        missing = [sid for sid in wanted if sid not in available]
    else:
        missing = []
    return {
        "state": "ready" if not missing else "partial",
        "packages": packages,
        "missing_selectors": missing,
        "selector_ids": wanted,
        "family": family,
        "resolution": resolution,
    }


def selector_id_for_position(position):
    return _ORBITAL_SELECTOR_IDS.get(position_token(position))


def plan_runtime_packages(document, queue):
    """Resolve one deterministic package set from a validated receiver queue."""
    prefs = {
        "positions": list(queue.get("positions_labels", [])),
        "style": queue.get("style", DEFAULT_STYLE),
        "resolution": queue.get("resolution", DEFAULT_RESOLUTION),
    }
    explicit = list(queue.get("selector_ids", []))
    if explicit:
        wanted = explicit
    elif queue.get("mode") == UPDATE_MODE_SYNC_TV:
        wanted = []
        seen = set()
        for service in queue.get("services", []):
            sid = selector_id_for_position(service.get("position"))
            if sid and sid not in seen:
                seen.add(sid)
                wanted.append(sid)
    else:
        wanted = []
    family = family_for_style(prefs["style"])
    if not family:
        return {"state": "invalid-preferences", "packages": [], "errors": ["unsupported style"],
                "missing_selectors": [], "selector_ids": wanted, "family": None,
                "resolution": prefs["resolution"]}
    if prefs["resolution"] not in dict(RESOLUTIONS):
        return {"state": "invalid-preferences", "packages": [], "errors": ["invalid resolution"],
                "missing_selectors": [], "selector_ids": wanted, "family": family,
                "resolution": prefs["resolution"]}
    errors = validate_publication_manifest(document)
    if errors:
        return {"state": "invalid-manifest", "packages": [], "errors": errors}
    candidates = [p for p in document.get("packages", [])
                  if p.get("family") == family and p.get("resolution") == prefs["resolution"]]
    if wanted:
        wanted_set = set(wanted)
        packages = [p for p in candidates if p.get("selector_id") in wanted_set]
        available = set(p.get("selector_id") for p in packages)
        missing = [sid for sid in wanted if sid not in available]
    elif queue.get("mode") == UPDATE_MODE_SYNC_TV:
        # Empty selective input means there is nothing to synchronize. Never
        # reinterpret it as FULL/all-packages.
        packages = []
        missing = []
    else:
        packages = candidates
        missing = []
    packages = sorted(packages, key=lambda p: (p.get("selector_id", ""), p.get("filename", "")))
    return {
        "state": "ready" if not missing else "partial",
        "packages": packages,
        "missing_selectors": missing,
        "selector_ids": wanted,
        "family": family,
        "resolution": prefs["resolution"],
    }


def build_download_jobs(document, package_plan):
    """Turn a package plan into integrity-complete download jobs."""
    errors = validate_publication_manifest(document)
    if errors:
        return {"state": "invalid-manifest", "jobs": [], "errors": errors}
    if package_plan.get("state") not in ("ready", "partial"):
        return {"state": "invalid-plan", "jobs": [], "errors": ["package plan is not executable"]}
    part_meta = {p["filename"]: p for p in document.get("parts", []) if isinstance(p, dict)}
    delivery = document.get("delivery", "direct")
    jobs = []
    for package in package_plan.get("packages", []):
        job = {
            "selector_id": package["selector_id"],
            "family": package["family"],
            "resolution": package["resolution"],
            "filename": package["filename"],
            "bytes": package["bytes"],
            "sha256": package["sha256"],
            "parts": [],
        }
        if delivery == "raw-github-parts":
            for url in package.get("parts", []):
                name = str(url).rsplit("/", 1)[-1]
                meta = part_meta.get(name)
                if meta is None:
                    return {"state": "invalid-manifest", "jobs": [], "errors": ["part metadata not found"]}
                job["parts"].append({
                    "url": url, "filename": name,
                    "bytes": meta["bytes"], "sha256": meta["sha256"],
                })
        else:
            job["parts"].append({
                "url": package["url"], "filename": package["filename"],
                "bytes": package["bytes"], "sha256": package["sha256"],
            })
        jobs.append(job)
    return {
        "state": "ready" if package_plan.get("state") == "ready" else "partial",
        "jobs": jobs,
        "missing_selectors": list(package_plan.get("missing_selectors", [])),
    }


def validate_destination(path):
    """Reject relative/root destinations; UI may only stage into a real subdirectory."""
    raw = str(path or "")
    if not os.path.isabs(raw):
        return None
    value = os.path.realpath(raw)
    if value == os.path.sep:
        return None
    protected = ("/bin", "/boot", "/dev", "/etc", "/lib", "/proc", "/root", "/run", "/sbin", "/sys", "/usr", "/var")
    if value in protected or any(value.startswith(p + os.path.sep) for p in protected):
        return None
    return value


def wanted_picon_names(queue):
    """Selective mode installs only receiver bouquet identities; FULL installs all."""
    if queue.get("mode") == UPDATE_MODE_FULL:
        return None
    names = set()
    for service in queue.get("services", []):
        stem = normalize_service_reference(service.get("service_reference", ""))
        if stem:
            names.add(stem + ".png")
    return names


def safe_archive_member(name):
    value = str(name or "").replace("\\", "/")
    if not value or value.startswith("/") or value.startswith("../") or "/../" in ("/" + value):
        return False
    base = value.rsplit("/", 1)[-1]
    return bool(base) and base not in (".", "..")


def runtime_publication():
    return {
        "persistent": bool(RUNTIME_PUBLICATION_ENABLED and RUNTIME_MANIFEST_URL),
        "manifest_url": RUNTIME_MANIFEST_URL if RUNTIME_PUBLICATION_ENABLED else None,
    }

def build_runtime_queue(preferences, enigma2_dir=ENIGMA2_DIR, publication=None):
    """Create the receiver action queue without performing network/filesystem writes."""
    prefs = dict(default_preferences())
    prefs.update(preferences or {})
    mode = prefs.get("update_mode", DEFAULT_UPDATE_MODE)
    if mode not in (UPDATE_MODE_SYNC_TV, UPDATE_MODE_FULL):
        raise ValueError("unsupported update mode")
    labels = list(prefs.get("positions", []) or [])
    selected = [position_token(x) for x in labels if position_token(x)]
    selectors = selected_selector_ids(labels)
    if mode == UPDATE_MODE_SYNC_TV:
        request = build_sync_request(
            enigma2_dir, selected, prefs.get("style", DEFAULT_STYLE),
            prefs.get("resolution", DEFAULT_RESOLUTION), include_radio=False)
        services = request["services"]
    else:
        services = []
    published = bool((publication or {}).get("persistent") and (publication or {}).get("manifest_url"))
    return {
        "state": READY if published else PUBLICATION_LOCKED,
        "mode": mode,
        "positions": selected,
        "positions_labels": labels,
        "selector_ids": selectors,
        "style": prefs.get("style", DEFAULT_STYLE),
        "resolution": prefs.get("resolution", DEFAULT_RESOLUTION),
        "destination": prefs.get("destination"),
        "services": services,
        "service_count": len(services),
        "manifest_url": (publication or {}).get("manifest_url"),
    }


def build_service_index(entries):
    """Index package entries by canonical service reference and expose collisions."""
    index = {}
    collisions = {}
    for entry in entries or []:
        stem = normalize_service_reference(entry.get("service_reference", ""))
        if not stem:
            continue
        candidate = dict(entry)
        candidate["service_reference"] = stem
        previous = index.get(stem)
        if previous is None:
            index[stem] = candidate
            continue
        if previous == candidate:
            continue
        bucket = collisions.setdefault(stem, [previous])
        if candidate not in bucket:
            bucket.append(candidate)
    for stem in collisions:
        index.pop(stem, None)
    return index, collisions


def resolve_service_entry(index, collisions, service_reference):
    """Never guess across a collision: ambiguous identities are explicitly blocked."""
    stem = normalize_service_reference(service_reference)
    if not stem:
        return {"state": "invalid-service-reference", "service_reference": ""}
    if stem in (collisions or {}):
        return {"state": "collision-blocked", "service_reference": stem,
                "candidates": list(collisions[stem])}
    entry = (index or {}).get(stem)
    if entry is None:
        return {"state": "missing", "service_reference": stem}
    return {"state": "matched", "service_reference": stem, "entry": entry}


_ALLOWED_MANIFEST_HOSTS = ("raw.githubusercontent.com",)
_PRODUCTION_PREFIX = "/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/"
_FAMILIES = ("channel-transparent", "channel-black", "channel-white")
_SHA256_RE = re.compile("^[0-9a-f]{64}$")
_FILENAME_RE = re.compile("^[A-Za-z0-9._-]+[.](?:zip|7z)$")

def _trusted_https_url(url):
    try:
        parsed = urlparse(str(url))
    except Exception:
        return False
    return (parsed.scheme == "https" and parsed.hostname in _ALLOWED_MANIFEST_HOSTS
            and not parsed.username and not parsed.password
            and parsed.path.startswith(_PRODUCTION_PREFIX)
            and not parsed.query and not parsed.fragment)


def validate_publication_manifest(document):
    """Validate the receiver-facing Warder manifest before any download is queued."""
    errors = []
    if not isinstance(document, dict):
        return ["manifest is not an object"]
    if document.get("schema") != 1:
        errors.append("unsupported manifest schema")
    generated = document.get("generated_from")
    if not isinstance(generated, dict) or generated.get("repository") != "Evolution-by-Warder/PiconHub-Warder-Evolution":
        errors.append("unexpected manifest source")
    elif len(str(generated.get("ref", ""))) < 7:
        errors.append("invalid source ref")
    delivery = document.get("delivery", "direct")
    if delivery not in ("direct", "raw-github-parts"):
        errors.append("unsupported delivery")
    packages = document.get("packages")
    if not isinstance(packages, list) or not packages:
        errors.append("packages missing")
        return errors
    seen = set()
    part_meta = {}
    if delivery == "raw-github-parts":
        parts = document.get("parts")
        if not isinstance(parts, list) or not parts:
            errors.append("part metadata missing")
        else:
            for part in parts:
                name = part.get("filename", "") if isinstance(part, dict) else ""
                size = part.get("bytes", 0) if isinstance(part, dict) else 0
                sha = part.get("sha256", "") if isinstance(part, dict) else ""
                if not name or name in part_meta or not isinstance(size, int) or size < 1 or size > 20 * 1024 * 1024 or not _SHA256_RE.match(str(sha)):
                    errors.append("invalid part metadata")
                    continue
                part_meta[name] = (size, sha)
    referenced_parts = set()
    for package in packages:
        if not isinstance(package, dict):
            errors.append("invalid package")
            continue
        key = (package.get("selector_id"), package.get("family"), package.get("resolution"))
        if key in seen:
            errors.append("duplicate selector/family/resolution")
        seen.add(key)
        if package.get("family") not in _FAMILIES:
            errors.append("invalid family")
        resolution = str(package.get("resolution", ""))
        if not re.match(r"^[1-9][0-9]*x[1-9][0-9]*$", resolution):
            errors.append("invalid package resolution")
        name = str(package.get("filename", ""))
        if not _FILENAME_RE.match(name):
            errors.append("invalid package filename")
        size = package.get("bytes", 0)
        if not isinstance(size, int) or size < 1:
            errors.append("invalid package size")
        if not _SHA256_RE.match(str(package.get("sha256", ""))):
            errors.append("invalid package sha256")
        if delivery == "direct":
            if not _trusted_https_url(package.get("url", "")):
                errors.append("untrusted package url")
        else:
            urls = package.get("parts")
            if not isinstance(urls, list) or not urls:
                errors.append("package parts missing")
                continue
            package_part_names = set()
            package_part_bytes = 0
            for url in urls:
                if not _trusted_https_url(url):
                    errors.append("untrusted part url")
                    continue
                part_name = str(url).rsplit("/", 1)[-1]
                expected_part_name = name + ".part%02d" % len(package_part_names)
                if part_name != expected_part_name:
                    errors.append("non-canonical package part")
                    continue
                if part_name in package_part_names:
                    errors.append("duplicate package part")
                    continue
                package_part_names.add(part_name)
                if part_name not in part_meta:
                    errors.append("part metadata not found")
                else:
                    package_part_bytes += part_meta[part_name][0]
                referenced_parts.add(part_name)
            if isinstance(size, int) and size > 0 and package_part_bytes != size:
                errors.append("package part size mismatch")
    if delivery == "raw-github-parts" and part_meta and referenced_parts != set(part_meta):
        errors.append("part metadata/reference mismatch")
    return errors


def publication_from_manifest(manifest_url, document):
    """Return runtime publication evidence only after strict manifest validation."""
    errors = validate_publication_manifest(document)
    if not _trusted_https_url(manifest_url):
        errors.append("untrusted manifest url")
    return {
        "persistent": not errors,
        "manifest_url": manifest_url if not errors else None,
        "delivery": document.get("delivery", "direct") if isinstance(document, dict) else None,
        "errors": errors,
    }
