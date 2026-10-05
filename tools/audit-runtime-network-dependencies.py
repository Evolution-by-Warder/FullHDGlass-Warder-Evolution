#!/usr/bin/env python3
"""Inventory network endpoints used by the shipped Warder runtime.

This is deliberately a classification gate, not a generic URL ban:
- Warder GitHub raw endpoints are first-party delivery/update authority.
- Preserved legacy picon archives are delivered from the pinned Warder/Trezor raw GitHub path; picon.cz is forbidden in shipped runtime.
- Open-Meteo, iTunes and TMDB are functional APIs, not legacy HDGlass FTP.
Any new host must be reviewed and classified here before CI accepts it.
"""
from pathlib import Path
from urllib.parse import urlparse
import ast, io, json, re, sys, tokenize

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "source/package-root"
OUT = ROOT / "assets/warder/runtime-network-dependencies.json"

HOST_CLASS = {
    "raw.githubusercontent.com": "WARDER_GITHUB_AND_PINNED_ARCHIVE",
    "geocoding-api.open-meteo.com": "FUNCTIONAL_API",
    "api.open-meteo.com": "FUNCTIONAL_API",
    "itunes.apple.com": "FUNCTIONAL_API",
    "www.imdb.com": "FUNCTIONAL_METADATA",
    "api.themoviedb.org": "FUNCTIONAL_API",
    "image.tmdb.org": "FUNCTIONAL_API",
}
URL_RE = re.compile(r"""https?://[^\s"'<>]+""")
def _python_runtime_text(source):
    """Ignore Python comments and standalone string expressions."""
    lines = source.splitlines(True)
    masked = [False] * len(lines)

    tree = ast.parse(source)
    nodes = [tree]
    while nodes:
        node = nodes.pop()
        nodes.extend(child for child in ast.iter_child_nodes(node))
        value = getattr(node, "value", None)
        if (isinstance(node, ast.Expr) and isinstance(value, ast.Constant)
                and isinstance(value.value, str)):
            start = getattr(node, "lineno", 1) - 1
            end = getattr(node, "end_lineno", start + 1)
            for index in range(start, min(end, len(masked))):
                masked[index] = True

    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT:
            start = token.start[0] - 1
            end = token.end[0]
            for index in range(start, min(end, len(masked))):
                masked[index] = True

    return "".join("\\n" if masked[index] and line.endswith("\\n") else
                   "" if masked[index] else line
                   for index, line in enumerate(lines))


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
    scan_text = _python_runtime_text(text) if path.suffix.lower() == ".py" else text
    if re.search(r"ftp://", scan_text, re.I):
        legacy_ftp.append(str(path.relative_to(ROOT)))
    for m in URL_RE.finditer(scan_text):
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
if picon:
    errors.append("picon.cz must not remain in shipped runtime")
if errors:
    for error in errors:
        print("ERROR:", error)
    sys.exit(1)
print("PASS runtime network dependency audit: %d classified hosts; picon.cz absent; no ftp:// runtime references" % len(found))
