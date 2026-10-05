# -*- coding: utf-8 -*-
"""FullHDGlass17 Warder Evolution - receiver driven picon synchronisation.

Pure planning helpers live here so the Enigma2 GUI can stay small.  No network
or GUI side effects are performed by this module.
"""
from __future__ import absolute_import

import os
import re

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
