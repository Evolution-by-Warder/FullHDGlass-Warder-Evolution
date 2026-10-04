#!/usr/bin/env python3
"""Inventory network endpoints used by the shipped Warder runtime.

This is deliberately a classification gate, not a generic URL ban:
- Warder GitHub raw endpoints are first-party delivery/update authority.
- picon.cz is the one isolated legacy channel-picon dependency pending cut-over.
- Open-Meteo, iTunes and TMDB are functional APIs, not legacy HDGlass FTP.
Any new host must be reviewed and classified here before CI accepts it.
"""
from pathlib import Path
from urllib.parse import urlparse
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "source/package-root"
OUT = ROOT / "assets/warder/runtime-network-dependencies.json"

HOST_CLASS = {
    "raw.githubusercontent.com": "WARDER_GITHUB",
    "picon.cz": "LEGACY_PICON_CHANNEL_SOURCE",
    "geocoding-api.open-meteo.com": "FUNCTIONAL_API",
    "api.open-meteo.com": "FUNCTIONAL_API",
    "itunes.apple.com": "FUNCTIONAL_API",
    "api.themoviedb.org": "FUNCTIONAL_API",
    "image.tmdb.org": "FUNCTIONAL_API",
}
URL_RE = re.compile(r"https?://[^\\s\\\"'<>]+")
found = {}
legacy_ftp = []
unknown = []
for path in sorted(SCAN.rglob("*")):
    if not path.is_file() or path.suffix.lower() not in {".py",".xml",".txt",".json",".sh"}:
        continue
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        continue
    if re.search(r"ftp://", text, re.I):
        legacy_ftp.append(str(path.relative_to(ROOT)))
    for m in URL_RE.finditer(text):
        url = m.group(0).rstrip("),.;")
        host = (urlparse(url).hostname or "").lower()
        cls = HOST_CLASS.get(host, "UNCLASSIFIED")
        rec = found.setdefault(host, {"classification": cls, "references": []})
        rel = str(path.relative_to(ROOT))
        line = text.count("\n", 0, m.start()) + 1
        ref = {"path": rel, "line": line, "url": url}
        if ref not in rec["references"]:
            rec["references"].append(ref)
        if cls == "UNCLASSIFIED":
            unknown.append("%s:%d %s" % (rel, line, url))

report = {
    "schema": 1,
    "policy": "All shipped runtime network hosts must be explicitly classified; legacy HDGlass FTP is forbidden.",
    "hosts": found,
}
# Preserve build/provenance metadata maintained in the committed audit document.
if OUT.exists():
    try:
        previous = json.loads(OUT.read_text(encoding="utf-8"))
        for key in ("channel_picon_build",):
            if key in previous:
                report[key] = previous[key]
    except Exception:
        pass
OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

errors = []
if legacy_ftp:
    errors.append("legacy FTP references: " + ", ".join(legacy_ftp))
if unknown:
    errors.append("unclassified network endpoints:\n  " + "\n  ".join(unknown))
picon = found.get("picon.cz", {}).get("references", [])
if len(picon) != 1 or not picon[0]["path"].endswith("setupGlass17/plugin.py"):
    errors.append("picon.cz must remain one isolated plugin.py dependency until Warder channel-package cut-over")
if errors:
    for error in errors:
        print("ERROR:", error)
    sys.exit(1)
print("PASS runtime network dependency audit: %d classified hosts; %d isolated picon.cz reference(s); no ftp:// runtime references" % (len(found), len(picon)))
