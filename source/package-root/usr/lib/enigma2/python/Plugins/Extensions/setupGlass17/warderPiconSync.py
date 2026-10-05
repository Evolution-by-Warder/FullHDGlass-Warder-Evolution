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
    fields = ref.split(":")
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
        if selected and position and position.lower() not in selected:
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
    ("400x240", "400 x 240"),
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

def build_runtime_queue(preferences, enigma2_dir=ENIGMA2_DIR, publication=None):
    """Create the receiver action queue without performing network/filesystem writes."""
    prefs = dict(default_preferences())
    prefs.update(preferences or {})
    mode = prefs.get("update_mode", DEFAULT_UPDATE_MODE)
    if mode not in (UPDATE_MODE_SYNC_TV, UPDATE_MODE_FULL):
        raise ValueError("unsupported update mode")
    selected = [position_token(x) for x in prefs.get("positions", []) if position_token(x)]
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
_FAMILIES = ("channel-transparent", "channel-black", "channel-white")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_FILENAME_RE = re.compile(r"^[A-Za-z0-9._-]+\\.(?:zip|7z)$")


def _trusted_https_url(url):
    try:
        parsed = urlparse(str(url))
    except Exception:
        return False
    return parsed.scheme == "https" and parsed.hostname in _ALLOWED_MANIFEST_HOSTS and not parsed.username and not parsed.password


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
                if not name or name in part_meta or not isinstance(size, int) or size < 1 or not _SHA256_RE.match(str(sha)):
                    errors.append("invalid part metadata")
                    continue
                part_meta[name] = (size, sha)
    referenced_parts = set()
    for package in packages:
        if not isinstance(package, dict):
            errors.append("invalid package")
            continue
        key = (package.get("selector_id"), package.get("family"))
        if key in seen:
            errors.append("duplicate selector/family")
        seen.add(key)
        if package.get("family") not in _FAMILIES:
            errors.append("invalid family")
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
            for url in urls:
                if not _trusted_https_url(url):
                    errors.append("untrusted part url")
                    continue
                part_name = str(url).rsplit("/", 1)[-1]
                if part_name not in part_meta:
                    errors.append("part metadata not found")
                referenced_parts.add(part_name)
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
