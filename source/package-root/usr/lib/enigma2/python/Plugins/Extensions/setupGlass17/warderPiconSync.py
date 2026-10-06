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
RUNTIME_MANIFEST_URL = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/picons/channels/test-candidate/manifest.json"
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


def position_token(position):
    """Normalize a canonical orbital token only; display labels are not parsed."""
    text = str(position or "").strip().lower()
    if text in ("dtt", "eee"):
        return "dtt"
    if re.match(r"^[0-9]+(?:\.[0-9]+)?[ew]$", text):
        return text
    return text


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
    if not selected:
        raise ValueError("no-satellite-position-selected")
    services = []
    for stem in bouquet_services(enigma2_dir, include_radio):
        position = service_orbital_position(stem.replace("_", ":"))
        if selected and (not position or position.lower() not in selected):
            continue
        services.append({"service_reference": stem, "position": position})
    return {
        "mode": UPDATE_MODE_SYNC_TV_RADIO if include_radio else UPDATE_MODE_SYNC_TV,
        "style": style,
        "resolution": resolution,
        "services": services,
    }


UPDATE_MODE_SYNC_TV = "sync-tv-lists"
UPDATE_MODE_SYNC_TV_RADIO = "sync-tv-radio-lists"
UPDATE_MODE_REPLACE_ALL = "replace-all-selected"
UPDATE_MODE_INCREMENTAL = "incremental-selected"
# Kept for source compatibility with TEST195 callers; its package-copy mode is
# now explicitly named incremental rather than the ambiguous legacy "FULL".
UPDATE_MODE_FULL = UPDATE_MODE_INCREMENTAL
DEFAULT_UPDATE_MODE = None
DEFAULT_STYLE = None
DEFAULT_RESOLUTION = None
DEFAULT_DESTINATION = "/usr/share/enigma2/picon"
CHANNEL_RESOLUTION_CHOICES = (
    ("50x30", "50 x 30 - Mini picons"),
    ("220x132", "220 x 132 - XPicons"),
    ("400x240", "400 x 240 - Large picons"),
)
AUXILIARY_ASSET_KEYS = (
    "piconProv-220", "piconProv-b", "piconProv-w",
    "piconSat-220", "piconSat-b", "piconSat-w",
    "piconCam-b", "piconCam-w",
    "piconWeather-b", "piconWeather-w",
)
PICON_DESTINATIONS = (
    ("/usr/share/enigma2/picon", "Receiver memory"),
    ("/media/hdd/picon", "Hard disk"),
    ("/media/usb/picon", "USB storage"),
    ("/media/sdcard/picon", "SD card"),
    ("/media/mmc/picon", "MMC storage"),
    ("/picon", "Root picon directory"),
)

UPDATE_MODES = (
    (UPDATE_MODE_SYNC_TV, "Synchronize with TV lists"),
    (UPDATE_MODE_SYNC_TV_RADIO, "Synchronize with TV and radio lists"),
    (UPDATE_MODE_REPLACE_ALL, "Copy all; replace current selected-position picons"),
    (UPDATE_MODE_INCREMENTAL, "Copy all; incremental update"),
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


# Genuine delivery options recovered from the pinned FullHDGlass/Trezor catalog.
# 220x132 transparent/black/white is the native Warder channel package triad.
CHANNEL_RESOLUTION_STYLES = {
    "50x30": ("black", "white"),
    "150x90": ("black", "white"),
    "220x132": ("transparent", "black", "white"),
    "400x240": ("transparent",),
}
LEGACY_CHANNEL_ARCHIVE_COLUMNS = {
    ("400x240", "transparent"): 3,
    ("50x30", "black"): 4,
    ("150x90", "black"): 5,
    ("50x30", "white"): 6,
    ("150x90", "white"): 7,
    ("220x132", "transparent"): 9,
}
LEGACY_CHANNEL_DESTINATIONS = {
    "50x30": "picon_50x30",
    "150x90": "picon",
    "220x132": "picon_220x132",
    "400x240": "picon_400x240",
}


def channel_style_supported(resolution, style):
    return style in CHANNEL_RESOLUTION_STYLES.get(str(resolution), ())


def channel_delivery_backend(resolution, style):
    if not channel_style_supported(resolution, style):
        return None
    return "warder" if resolution == "220x132" else "pinned-legacy"


def legacy_channel_archive_column(resolution, style):
    return LEGACY_CHANNEL_ARCHIVE_COLUMNS.get((str(resolution), str(style)))


def legacy_channel_destination(resolution):
    return LEGACY_CHANNEL_DESTINATIONS.get(str(resolution))


def plan_legacy_channel_archives(selected_selector_ids, satlist, resolution, style):
    """Resolve explicit selector IDs to the matching pinned SATLIST archive column."""
    selectors = list(selected_selector_ids or [])
    if not valid_position_selection(selectors):
        raise ValueError("no-satellite-position-selected")
    column = legacy_channel_archive_column(resolution, style)
    if column is None:
        raise ValueError("no-pinned-channel-archive-for-resolution-and-colour")
    by_selector = {}
    for row in satlist or []:
        if not row:
            continue
        selector = selector_id_for_display_label(row[0])
        if not selector:
            continue
        if selector in by_selector:
            raise ValueError("ambiguous-satellite-package-selector")
        by_selector[selector] = row
    result = []
    seen_ids = set()
    for selector in selectors:
        row = by_selector.get(selector)
        if row is None or len(row) <= column:
            raise ValueError("satellite-position-not-in-pinned-archive-catalog")
        archive_id = str(row[column] or "").strip()
        if not re.match(r"^[0-9]{1,5}$", archive_id):
            raise ValueError("pinned-channel-archive-not-available-for-selected-position")
        if archive_id in seen_ids:
            raise ValueError("duplicate-pinned-channel-archive")
        seen_ids.add(archive_id)
        result.append((selector, archive_id))
    return result


def default_preferences(destination=DEFAULT_DESTINATION):
    return {
        "positions": [],
        "package_selectors": [],
        "position_bindings": [],
        "resolution": None,
        "style": None,
        "destination": destination or DEFAULT_DESTINATION,
        "update_mode": None,
        "prepared": False,
    }


def reset_working_preferences(preferences=None):
    """Return the deliberate empty state used after a fully successful action."""
    return default_preferences(DEFAULT_DESTINATION)


def preferences_after_task(preferences, outcome):
    """Reset only after success; Cancel and Error retain a retryable snapshot."""
    state = str(outcome or "").lower()
    if state == "success":
        return reset_working_preferences(preferences)
    if state in ("cancel", "error"):
        return dict(preferences or {})
    raise ValueError("unknown Warder task outcome")


def set_task_position_bindings(preferences, bindings):
    result = dict(default_preferences())
    result.update(preferences or {})
    original = list(bindings or [])
    normalized = normalize_position_bindings(original)
    if len(normalized) != len(original):
        normalized = []
    result["position_bindings"] = normalized
    result["positions"] = task_positions_from_bindings(normalized)
    result["package_selectors"] = task_package_selectors_from_bindings(normalized)
    result["prepared"] = bool(normalized)
    return result


def channel_preferences_ready(preferences):
    prefs = dict(preferences or {})
    return bool(valid_task_selection(prefs)
                and prefs.get("resolution") in ("50x30", "220x132", "400x240")
                and prefs.get("style") in dict(STYLES)
                and channel_style_supported(prefs.get("resolution"), prefs.get("style"))
                and prefs.get("update_mode") in dict(UPDATE_MODES)
                and validate_destination(prefs.get("destination")))


def auxiliary_variants(asset_keys):
    """List only real catalog-backed variants, in a stable color order."""
    definitions = {
        "piconProv": (("piconProv-220", "Transparent"), ("piconProv-b", "Black"), ("piconProv-w", "White")),
        "piconSat": (("piconSat-220", "Transparent"), ("piconSat-b", "Black"), ("piconSat-w", "White")),
        "piconCam": (("piconCam-220", "Transparent"), ("piconCam-b", "Black"), ("piconCam-w", "White")),
        "piconWeather": (("piconWeather-220", "Transparent"), ("piconWeather-b", "Black"), ("piconWeather-w", "White")),
    }
    available = set(asset_keys or [])
    return {kind: tuple((key, label) for key, label in options if key in available)
            for kind, options in definitions.items()}


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
_SELECTOR_LABEL_BINDINGS = {
    "(0.8W) Freesat": (
        "FREESAT",
        "0.8w"
    ),
    "(0.8W) Digi / Telly": (
        "DIGI_TELLY",
        "0.8w"
    ),
    "(16.0E) Antiksat": (
        "ANTIKSAT",
        "16.0e"
    ),
    "(23.5E) Skylink": (
        "SKYLINK",
        "23.5e"
    ),
    "DVB-T sk/cz": (
        "DVB-T-SK-CZ",
        "dtt"
    ),
    "(45.0W) Intelsat 14 (IS-14)": (
        "450W",
        "45.0w"
    ),
    "(30.0W) Hispasat 1D,1E": (
        "300W",
        "30.0w"
    ),
    "(27.5W) Intelsat 907": (
        "275W",
        "27.5w"
    ),
    "(24.5W) AlcomSat 1": (
        "248W",
        "24.5w"
    ),
    "(22.0W) SES 4": (
        "220W",
        "22.0w"
    ),
    "(15.0W) Telstar 12": (
        "150W",
        "15.0w"
    ),
    "(14.0W) Express AM8": (
        "140W",
        "14.0w"
    ),
    "(12.5W) Eutelsat 12 West A": (
        "125W",
        "12.5w"
    ),
    "(11.0W) Express AM44": (
        "110W",
        "11.0w"
    ),
    "(8.0W) Eutelsat 8 West B,D": (
        "80W",
        "8.0w"
    ),
    "(7.0W) Nilesat 102,201/Eutelsat 7 West A": (
        "70W",
        "7.0w"
    ),
    "(5.0W) Eutelsat 5 West A,B": (
        "50W",
        "5.0w"
    ),
    "(4.0W) Amos 2/Amos 3": (
        "40W",
        "4.0w"
    ),
    "(1.0W) Thor 5,6,7/Intelsat 10-02": (
        "10W",
        "1.0w"
    ),
    "(0.8W) Thor 5,6,7/Intelsat 10-02": (
        "08W",
        "0.8w"
    ),
    "(1.9E) BulgariaSat-1": (
        "19E",
        "1.9e"
    ),
    "(3.0E) Eutelsat 3B": (
        "30E",
        "3.0e"
    ),
    "(3.1E) Eutelsat 3B": (
        "31E",
        "3.1e"
    ),
    "(4.8E) SES 5/Astra 4A": (
        "48E_A",
        "4.8e"
    ),
    "(4.9E) SES 5/Astra 4A": (
        "48E_B",
        "4.9e"
    ),
    "(7.0E) Eutelsat 7A/7B": (
        "70E",
        "7.0e"
    ),
    "(9.0E) Eutelsat 9A": (
        "90E",
        "9.0e"
    ),
    "(10.0E) Eutelsat 10A": (
        "100E",
        "10.0e"
    ),
    "(13.0E) Hot Bird 13B/13C/13D": (
        "130E",
        "13.0e"
    ),
    "(16.0E) Eutelsat 16A": (
        "160E",
        "16.0e"
    ),
    "(19.2E) Astra 1KR,1L,1M,1N": (
        "192E",
        "19.2e"
    ),
    "(21.5E) Eutelsat 21B": (
        "216E",
        "21.5e"
    ),
    "(23.5E) Astra 3B": (
        "235E",
        "23.5e"
    ),
    "(26.0E) Badr 4,5,6": (
        "260E",
        "26.0e"
    ),
    "(28.2E) Astra 2A,2E,2F,2G": (
        "282E",
        "28.2e"
    ),
    "(30.5E) Arabsat 5A,6A": (
        "305E",
        "30.5e"
    ),
    "(31.5E) Astra 1G,5B": (
        "315E",
        "31.5e"
    ),
    "(33.0E) Eutelsat 33C": (
        "330E",
        "33.0e"
    ),
    "(36.0E) Eutelsat 36A,36B": (
        "360E",
        "36.0e"
    ),
    "(39.0E) Hellas Sat 2": (
        "390E",
        "39.0e"
    ),
    "(42.0E) Turksat 2A,3A,4A": (
        "420E",
        "42.0e"
    ),
    "(45.0E) Intelsat 12 (IS-12)": (
        "450E",
        "45.0e"
    ),
    "(46.0E) Azerspace-1": (
        "460E",
        "46.0e"
    ),
    "(51.5E) Belintersat 1": (
        "515E",
        "51.5e"
    ),
    "(52.0E) TurkmenAlem/MonacoSat": (
        "520E",
        "52.0e"
    ),
    "(52.5E) Yahsat 1A": (
        "525E",
        "52.5e"
    ),
    "(53.0E) Express AM6": (
        "530E",
        "53.0e"
    ),
    "(54.9E) Yamal 402": (
        "549E",
        "54.9e"
    ),
    "(56.0E) Express AT1": (
        "560E",
        "56.0e"
    ),
    "(62.0E) Intelsat 902": (
        "620E",
        "62.0e"
    ),
    "(66.0E) Intelsat 17": (
        "660E",
        "66.0e"
    ),
    "(68.5E) Intelsat 20 (IS-20)": (
        "685E",
        "68.5e"
    ),
    "(70.5E) Eutelsat 70B": (
        "705E",
        "70.5e"
    ),
    "(74.9E) ABS 2/ABS 2A": (
        "749E",
        "74.9e"
    ),
    "(75.0E) ABS 2/ABS 2A": (
        "750E",
        "75.0e"
    ),
    "(85.0E) Intelsat 15/Horizons 2": (
        "850E",
        "85.0e"
    ),
    "(85.1E) Intelsat 15/Horizons 2": (
        "851E",
        "85.1e"
    ),
    "(0.8W) Digi/Telly": (
        "DIGI_TELLY",
        "0.8w"
    )
}
_SELECTOR_ID_TO_POSITION = {
    "FREESAT": "0.8w",
    "DIGI_TELLY": "0.8w",
    "ANTIKSAT": "16.0e",
    "SKYLINK": "23.5e",
    "DVB-T-SK-CZ": "dtt",
    "450W": "45.0w",
    "300W": "30.0w",
    "275W": "27.5w",
    "248W": "24.5w",
    "220W": "22.0w",
    "150W": "15.0w",
    "140W": "14.0w",
    "125W": "12.5w",
    "110W": "11.0w",
    "80W": "8.0w",
    "70W": "7.0w",
    "50W": "5.0w",
    "40W": "4.0w",
    "10W": "1.0w",
    "08W": "0.8w",
    "19E": "1.9e",
    "30E": "3.0e",
    "31E": "3.1e",
    "48E_A": "4.8e",
    "48E_B": "4.9e",
    "70E": "7.0e",
    "90E": "9.0e",
    "100E": "10.0e",
    "130E": "13.0e",
    "160E": "16.0e",
    "192E": "19.2e",
    "216E": "21.5e",
    "235E": "23.5e",
    "260E": "26.0e",
    "282E": "28.2e",
    "305E": "30.5e",
    "315E": "31.5e",
    "330E": "33.0e",
    "360E": "36.0e",
    "390E": "39.0e",
    "420E": "42.0e",
    "450E": "45.0e",
    "460E": "46.0e",
    "515E": "51.5e",
    "520E": "52.0e",
    "525E": "52.5e",
    "530E": "53.0e",
    "549E": "54.9e",
    "560E": "56.0e",
    "620E": "62.0e",
    "660E": "66.0e",
    "685E": "68.5e",
    "705E": "70.5e",
    "749E": "74.9e",
    "750E": "75.0e",
    "850E": "85.0e",
    "851E": "85.1e"
}

def position_binding(selector_id):
    """Return the immutable orbital binding for an explicit package selector ID."""
    selector = str(selector_id or "").strip()
    position = _SELECTOR_ID_TO_POSITION.get(selector)
    if not position:
        return None
    return {"selector_id": selector, "orbital_position": position}

def selector_id_for_display_label(label):
    """Attach a stable selector ID while constructing a GUI item; never use its label later."""
    pair = _SELECTOR_LABEL_BINDINGS.get(str(label or "").strip())
    return pair[0] if pair else None

def canonical_position_for_selector(selector_id):
    """Resolve a technical package selector through the explicit domain binding."""
    return _SELECTOR_ID_TO_POSITION.get(str(selector_id or ""))


def task_binding_for_display_label(label):
    """Capture canonical position and technical selector when creating a GUI item."""
    pair = _SELECTOR_LABEL_BINDINGS.get(str(label or "").strip())
    if not pair:
        return None
    selector, position = pair
    return {"canonical_position": position_token(position).upper(), "package_selector": selector}


def task_binding_for_package_selector(package_selector):
    """Create an explicit task binding from a known package selector."""
    selector = str(package_selector or "").strip()
    position = canonical_position_for_selector(selector)
    if not position:
        return None
    return {"canonical_position": position_token(position).upper(), "package_selector": selector}


def normalize_position_bindings(bindings):
    """Validate task bindings without deriving identity from display text."""
    result = []
    seen = set()
    for item in bindings or []:
        if not isinstance(item, dict):
            return []
        selector = str(item.get("package_selector") or "").strip()
        canonical = position_token(item.get("canonical_position")).upper()
        expected = canonical_position_for_selector(selector)
        if not selector or not expected or canonical != position_token(expected).upper() or selector in seen:
            return []
        seen.add(selector)
        result.append({"canonical_position": canonical, "package_selector": selector})
    return result


def task_positions_from_bindings(bindings):
    result = []
    seen = set()
    for item in normalize_position_bindings(bindings):
        position = item["canonical_position"]
        if position not in seen:
            seen.add(position)
            result.append(position)
    return result


def task_package_selectors_from_bindings(bindings):
    return [item["package_selector"] for item in normalize_position_bindings(bindings)]


def position_bindings_for_preferences(preferences):
    """Validate canonical task positions and separate package selectors as one state."""
    prefs = dict(preferences or {})
    bindings = normalize_position_bindings(prefs.get("position_bindings"))
    if not bindings:
        return []
    if list(prefs.get("positions", []) or []) != task_positions_from_bindings(bindings):
        return []
    if list(prefs.get("package_selectors", []) or []) != task_package_selectors_from_bindings(bindings):
        return []
    return bindings


def valid_task_selection(preferences):
    return bool(position_bindings_for_preferences(preferences))


def task_positions_for_display(preferences):
    """Expose only the already-selected canonical task positions to the GUI."""
    if not valid_task_selection(preferences):
        return []
    return list((preferences or {}).get("positions", []))


def package_display_name(package_selector):
    """Return display-only text for a package after its canonical binding is known."""
    selector = str(package_selector or "").strip()
    for label, pair in _SELECTOR_LABEL_BINDINGS.items():
        if pair[0] == selector:
            return label.split(") ", 1)[1] if label.startswith("(") and ") " in label else label
    return ""



def selected_selector_ids(selector_ids):
    result = []
    seen = set()
    for selector in selector_ids or []:
        binding = position_binding(selector)
        sid = binding.get("selector_id") if binding else None
        if sid and sid not in seen:
            seen.add(sid)
            result.append(sid)
    return result


def valid_position_selection(selector_ids):
    """Accept only explicit package selector IDs attached to GUI items."""
    values = [str(x).strip() for x in (selector_ids or []) if str(x).strip()]
    if not values or len(set(values)) != len(values):
        return False
    return all(position_binding(selector) for selector in values)


def family_for_style(style):
    return {
        "transparent": "channel-transparent",
        "black": "channel-black",
        "white": "channel-white",
    }.get(style)


def select_manifest_packages(document, preferences):
    """Select exact packages from explicit task positions and package selectors."""
    errors = validate_publication_manifest(document)
    if errors:
        return {"state": "invalid-manifest", "packages": [], "errors": errors}
    prefs = dict(default_preferences())
    prefs.update(preferences or {})
    if not valid_task_selection(prefs):
        return {"state": "invalid-selection", "packages": [], "errors": ["no-satellite-position-selected"]}
    family = family_for_style(prefs.get("style"))
    if not family:
        return {"state": "unsupported-style", "packages": [], "errors": ["unsupported style"]}
    wanted = selected_selector_ids(prefs.get("package_selectors"))
    resolution = prefs.get("resolution", DEFAULT_RESOLUTION)
    packages = [p for p in document.get("packages", [])
                if p.get("family") == family and p.get("resolution") == resolution]
    wanted_set = set(wanted)
    packages = [p for p in packages if p.get("selector_id") in wanted_set]
    available = set(p.get("selector_id") for p in packages)
    missing = [sid for sid in wanted if sid not in available]
    return {
        "state": "ready" if not missing else "partial",
        "packages": packages,
        "missing_selectors": missing,
        "selector_ids": wanted,
        "positions": list(prefs.get("positions", [])),
        "family": family,
        "resolution": resolution,
    }


def selector_id_for_position(position):
    value = position_token(position)
    for selector, canonical in _SELECTOR_ID_TO_POSITION.items():
        if canonical == value and selector not in ("FREESAT", "DIGI_TELLY", "ANTIKSAT", "SKYLINK"):
            return selector
    return None


def plan_runtime_packages(document, queue):
    """Resolve packages only when canonical positions and selectors agree."""
    selectors = list(queue.get("package_selectors", []))
    task_bindings = normalize_position_bindings(queue.get("position_bindings", []))
    prefs = {
        "positions": list(queue.get("positions", [])),
        "package_selectors": selectors,
        "position_bindings": task_bindings,
        "style": queue.get("style", DEFAULT_STYLE),
        "resolution": queue.get("resolution", DEFAULT_RESOLUTION),
    }
    if not task_bindings or not valid_position_selection(selectors):
        return {"state": "invalid-selection", "packages": [], "errors": ["no-satellite-position-selected"],
                "missing_selectors": [], "selector_ids": [], "family": family_for_style(prefs["style"]),
                "resolution": prefs["resolution"]}
    binding_selectors = task_package_selectors_from_bindings(task_bindings)
    derived_positions = set(position_token(x) for x in task_positions_from_bindings(task_bindings))
    explicit_positions = set(position_token(x) for x in queue.get("positions", []))
    if binding_selectors != selectors or explicit_positions != derived_positions:
        return {"state": "invalid-selection", "packages": [], "errors": ["selector-position-binding-mismatch"],
                "missing_selectors": [], "selector_ids": selectors, "family": family_for_style(prefs["style"]),
                "resolution": prefs["resolution"]}
    explicit = selectors
    if explicit:
        wanted = explicit
    elif queue.get("mode") in (UPDATE_MODE_SYNC_TV, UPDATE_MODE_SYNC_TV_RADIO):
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
    if not re.match(r"^[1-9][0-9]*x[1-9][0-9]*$", str(prefs["resolution"])):
        return {"state": "invalid-preferences", "packages": [], "errors": ["invalid resolution"],
                "missing_selectors": [], "selector_ids": wanted, "family": family,
                "resolution": prefs["resolution"]}
    errors = validate_publication_manifest(document)
    if errors:
        return {"state": "invalid-manifest", "packages": [], "errors": errors}
    selected_positions = derived_positions
    candidates = [p for p in document.get("packages", [])
                  if p.get("family") == family and p.get("resolution") == prefs["resolution"]
                  and (p.get("orbital_position") or canonical_position_for_selector(p.get("selector_id"))) in selected_positions]
    if wanted:
        wanted_set = set(wanted)
        packages = [p for p in candidates if p.get("selector_id") in wanted_set]
        available = set(p.get("selector_id") for p in packages)
        missing = [sid for sid in wanted if sid not in available]
    elif queue.get("mode") in (UPDATE_MODE_SYNC_TV, UPDATE_MODE_SYNC_TV_RADIO):
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
        selector = package["selector_id"]
        orbital_position = package.get("orbital_position") or canonical_position_for_selector(selector)
        job = {
            "selector_id": selector,
            "orbital_position": orbital_position,
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
    raw = os.path.normpath(str(path or ""))
    if not os.path.isabs(raw):
        return None
    value = os.path.realpath(raw)
    # Do not silently follow a user supplied symlink while installing files.
    if value != os.path.abspath(raw):
        return None
    probe = os.path.sep
    for component in [part for part in raw.split(os.path.sep) if part]:
        probe = os.path.join(probe, component)
        if os.path.islink(probe):
            return None
    if value == os.path.sep:
        return None
    if value == DEFAULT_DESTINATION:
        return value
    protected = ("/bin", "/boot", "/dev", "/etc", "/lib", "/proc", "/root", "/run", "/sbin", "/sys", "/usr", "/var")
    if value in protected or any(value.startswith(p + os.path.sep) for p in protected):
        return None
    return value


def destination_storage_available(path):
	"""Do not create a removable-storage preset on the receiver's root disk."""
	value = validate_destination(path)
	if not value:
		return False
	for mountpoint in ("/media/hdd", "/media/usb", "/media/sdcard", "/media/mmc"):
		if value == mountpoint or value.startswith(mountpoint + os.path.sep):
			return os.path.ismount(mountpoint)
	return True


def wanted_picon_names(queue):
    """Selective mode installs only receiver bouquet identities; FULL installs all."""
    if queue.get("mode") not in (UPDATE_MODE_SYNC_TV, UPDATE_MODE_SYNC_TV_RADIO):
        return None
    names = set()
    for service in queue.get("services", []):
        stem = normalize_service_reference(service.get("service_reference", ""))
        if stem:
            names.add(stem + ".png")
    return names


def classify_requested_picons(wanted, upstream_names, installed_names):
    """Scope sync results to selected package assets before reporting missing files."""
    upstream = set(upstream_names or [])
    installed = set(installed_names or [])
    if wanted is None:
        relevant = set(upstream)
        outside = set()
    else:
        requested = set(wanted or [])
        relevant = requested.intersection(upstream)
        outside = requested.difference(upstream)
    return {
        "relevant": relevant,
        "outside_selected_packages": outside,
        "missing": relevant.difference(installed),
    }


def plan_stale_position_picons(existing_names, selected_positions, package_names):
    """Select only stale PNG service identities for explicitly selected orbits."""
    selected = set(position_token(x) for x in (selected_positions or []) if x)
    if not selected:
        return []
    packages = set(package_names or [])
    stale = []
    for name in sorted(set(existing_names or [])):
        if not str(name).lower().endswith(".png") or name in packages:
            continue
        stem = normalize_service_reference(os.path.basename(str(name))[:-4].replace("_", ":"))
        position = service_orbital_position(stem.replace("_", ":")) if stem else None
        if position and position.lower() in selected:
            stale.append(str(name))
    return stale


def success_summary(updated, selected_services=None, translate=None):
    """Format localized result lines without ambiguous 'file(s)' wording."""
    translate = translate or (lambda message: message)
    count = int(updated)
    result = translate("%d picon successfully updated" if count == 1 else "%d picons successfully updated") % count
    if selected_services is not None:
        services = int(selected_services)
        result += "\n" + (translate("%d service selected" if services == 1 else "%d services selected") % services)
    return result


def package_result_summary(package_results, translate=None):
    """Format measured counts by selected package and canonical orbital position."""
    translate = translate or (lambda message: message)
    rows = sorted(package_results or [], key=lambda x: (str(x.get("orbital_position") or ""), str(x.get("selector_id") or "")))
    lines = []
    total_updated = 0
    total_failures = 0
    for row in rows:
        position = str(row.get("orbital_position") or "—").upper()
        selector = str(row.get("package_selector") or row.get("selector_id") or "")
        package_name = package_display_name(selector)
        updated = max(0, int(row.get("updated", 0)))
        failures = max(0, int(row.get("failures", 0)))
        total_updated += updated
        total_failures += failures
        lines.append(translate("%s / %s: %d picons updated; %d failures") % (position, package_name or translate("Package"), updated, failures))
    lines.append(translate("Total: %d picons updated") % total_updated)
    lines.append(translate("Failures: %d") % total_failures)
    if total_failures and total_updated:
        status = translate("PARTIAL SUCCESS")
    elif total_failures:
        status = translate("ERROR")
    else:
        status = translate("SUCCESSFUL")
    return {"status": status, "updated": total_updated, "failures": total_failures, "text": "\n".join(lines)}


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
    """Create a queue with canonical task positions and separate package selectors."""
    prefs = dict(default_preferences())
    prefs.update(preferences or {})
    mode = prefs.get("update_mode")
    bindings = position_bindings_for_preferences(prefs)
    if not bindings:
        raise ValueError("no-satellite-position-selected")
    selected = list(prefs.get("positions", []) or [])
    selectors = list(prefs.get("package_selectors", []) or [])
    if mode not in dict(UPDATE_MODES):
        raise ValueError("unsupported update mode")
    resolution = prefs.get("resolution")
    style = prefs.get("style")
    if resolution != "220x132":
        raise ValueError("non-native resolution requires pinned selected-position archives")
    if not channel_style_supported("220x132", style):
        raise ValueError("unsupported Warder channel picon colour")
    destination = validate_destination(prefs.get("destination"))
    if not destination:
        raise ValueError("invalid Warder picon destination")
    if mode in (UPDATE_MODE_SYNC_TV, UPDATE_MODE_SYNC_TV_RADIO):
        request = build_sync_request(
            enigma2_dir, selected, style, resolution,
            include_radio=(mode == UPDATE_MODE_SYNC_TV_RADIO))
        services = request["services"]
    else:
        services = []
    published = bool((publication or {}).get("persistent") and (publication or {}).get("manifest_url"))
    return {
        "state": READY if published else PUBLICATION_LOCKED,
        "mode": mode,
        "positions": selected,
        "package_selectors": selectors,
        "position_bindings": bindings,
        "style": style,
        "resolution": resolution,
        "destination": destination,
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
_ALLOWED_PUBLICATION_PREFIXES = (
    "/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/picons/channels/",
    "/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/picons/channels/test-candidate/",
)
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
            and any(parsed.path.startswith(prefix) for prefix in _ALLOWED_PUBLICATION_PREFIXES)
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
        selector = package.get("selector_id")
        declared_position = package.get("orbital_position")
        bound_position = canonical_position_for_selector(selector)
        if declared_position is not None and declared_position != bound_position:
            errors.append("incorrect canonical orbital position binding")
        key = (selector, package.get("family"), package.get("resolution"))
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
