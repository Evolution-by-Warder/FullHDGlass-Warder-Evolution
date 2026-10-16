#!/usr/bin/env python3
"""TEST206 receiver-only trust policy hotfix. No production branch changes."""
from pathlib import Path
import importlib.util
import json
import urllib.request
import sys
p = Path("/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderPiconSync.py")
if not p.is_file():
    raise SystemExit("ERROR: warderPiconSync.py not found")
old = p.read_bytes()
needle = b'AUXILIARY_PUBLICATION_SOURCES = {\n'
block = b'''    "fullhd-test": {
        "expected_origin": "raw.githubusercontent.com",
        "repository": "Evolution-by-Warder/FullHDGlass-Warder-Evolution",
        "ref": "warder-modernization-work",
        "pinned_commit": None,
        "manifest_url": "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads.json",
        "source_root": "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/",
        "package_root": "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/",
        "redirect_root": "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads/",
    },
'''
if b'"fullhd-test": {' not in old:
    if old.count(needle) != 1:
        raise SystemExit("ERROR: unexpected module layout, no changes made")
    new = old.replace(needle, needle + block)
    compile(new, str(p), "exec")
    backup = p.with_name(p.name + ".test206-backup")
    if not backup.exists():
        backup.write_bytes(old)
    p.write_bytes(new)
    print("Trusted test source added; backup saved.")
else:
    print("Trusted test source already present.")
spec = importlib.util.spec_from_file_location("warder_test_sync", str(p))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
url = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/ccf74604aa914a2a8fa3eacb79454ff1d8f9e867/assets/warder/downloads.json"
req = urllib.request.Request(url, headers={"User-Agent":"WARDER-TEST206-check"})
with urllib.request.urlopen(req, timeout=30) as response:
    catalog = json.loads(response.read().decode("utf-8-sig"))
for name in ("menuicons", "menuiconsbig"):
    asset = catalog["assets"][name]
    urls = asset.get("parts") or [asset["url"]]
    assert asset["publication_source_id"] == "fullhd-test", name
    assert all(mod.trusted_auxiliary_url(u, "fullhd-test") for u in urls), name
    print("PASS:", name, len(urls), "trusted archive URL(s)")
print("PASS: test catalog and both icon archive trust policies")
