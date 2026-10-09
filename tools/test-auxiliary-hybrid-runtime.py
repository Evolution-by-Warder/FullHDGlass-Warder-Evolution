#!/usr/bin/env python3
"""Focused hybrid auxiliary publication/runtime regressions."""
import ast
import hashlib
import importlib.util
import json
import os
import re
import struct
import tempfile
import zipfile
from pathlib import Path
from types import MethodType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
SYNC_PATH = PLUGIN_DIR / "warderPiconSync.py"
PLUGIN_PATH = PLUGIN_DIR / "plugin.py"
CATALOG_PATH = ROOT / "assets/warder/downloads.json"
CANDIDATE_FIXTURE = ROOT / "tools/fixtures/piconhub-candidate-downloads-db5eec9f1.json"

spec = importlib.util.spec_from_file_location("warder_hybrid_sync", str(SYNC_PATH))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)
catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
# This is the byte-for-byte candidate-downloads.json fetched from the exact
# PiconHub manifest commit in the runtime descriptor, not a synthesized fixture.
candidate_bytes = CANDIDATE_FIXTURE.read_bytes()
assert hashlib.sha256(candidate_bytes).hexdigest() == "ab32661c0ce0b73b19506d1bd4e8befa0dd47eaff267945f4887503514ee8d1d"
candidate = json.loads(candidate_bytes.decode("utf-8"))

assert sync.validate_auxiliary_candidate_manifest(candidate, sync.AUXILIARY_CANDIDATE_MANIFEST_URL) == []
assert sync.validate_auxiliary_hybrid_catalog(catalog, candidate) == []

# One visible Provider/Satellite variant always maps to exactly two jobs.
for kind, domain in (("provider", "piconProv"), ("satellite", "piconSat")):
    assert sync.auxiliary_hybrid_variants("piconProv" if kind == "provider" else "piconSat") == (
        ("transparent", "Transparent"), ("black", "Black"), ("white", "White"))
    for variant in ("transparent", "black", "white"):
        plan = sync.build_auxiliary_jobs(catalog, candidate, kind, variant)
        assert plan["state"] == "ready", (kind, variant, plan)
        jobs = plan["jobs"]
        assert len(jobs) == 2
        assert [job["layer"] for job in jobs] == ["legacy_fallback", "warder_safe_priority"]
        assert [job["destination"] for job in jobs] == [domain, domain + "_220x132"]
        assert jobs[0]["root"] == domain and jobs[1]["root"] == domain + "_220x132"

# The manifest is pinned to db5eec9; its archive URL fields record the exact
# historical publication ref 7387e9. Runtime catalog URLs are independently
# constructed and allowlisted at db5eec9, so the representations stay separate.
candidate_metadata_url = candidate["assets"]["piconProv-warder-safe-b"]["url"]
candidate_url = catalog["assets"]["piconProv-warder-safe-b"]["url"]
main_url = catalog["assets"]["piconProv-b"]["url"]
assert sync.trusted_auxiliary_url(candidate_url, "piconhub-aux-candidate")
assert sync.AUXILIARY_CANDIDATE_COMMIT in candidate_url
assert sync.AUXILIARY_CANDIDATE_MANIFEST_ARCHIVE_REF in candidate_metadata_url
assert not sync.trusted_auxiliary_url(candidate_metadata_url, "piconhub-aux-candidate")
assert not sync.trusted_auxiliary_url(main_url, "piconhub-aux-candidate")
assert sync.trusted_auxiliary_url(main_url, "fullhd-production")
assert not sync.trusted_auxiliary_url(candidate_url, "fullhd-production")
wrong_ref = candidate_url.replace(sync.AUXILIARY_CANDIDATE_COMMIT, "0" * 40)
assert not sync.trusted_auxiliary_url(wrong_ref, "piconhub-aux-candidate")
assert not sync.trusted_auxiliary_url(candidate_url + "/../other.zip", "piconhub-aux-candidate")
assert not sync.trusted_auxiliary_url(candidate_url + "?download=1", "piconhub-aux-candidate")

# Negative publication-source cases: wrong commit, repo, path, branch, and
# cross-source manifest URLs are rejected; the real pinned manifest passes above.
bad_manifest_urls = (
    sync.AUXILIARY_CANDIDATE_MANIFEST_URL.replace(sync.AUXILIARY_CANDIDATE_COMMIT, "0" * 40),
    sync.AUXILIARY_CANDIDATE_MANIFEST_URL.replace("PiconHub-Warder-Evolution", "Unrelated-Warder-Evolution"),
    sync.AUXILIARY_CANDIDATE_MANIFEST_URL.replace("auxiliary-hybrid-runtime-candidate-2026-10-07", "other-candidate"),
    sync.AUXILIARY_CANDIDATE_MANIFEST_URL.replace(sync.AUXILIARY_CANDIDATE_COMMIT, "warder-master-production"),
    main_url,
)
for bad_manifest_url in bad_manifest_urls:
    assert sync.validate_auxiliary_candidate_manifest(candidate, bad_manifest_url), bad_manifest_url
bad_url_replacements = (
    (sync.AUXILIARY_CANDIDATE_MANIFEST_ARCHIVE_REF, "0" * 40),
    (sync.AUXILIARY_CANDIDATE_MANIFEST_ARCHIVE_REF, sync.AUXILIARY_CANDIDATE_COMMIT),
    ("PiconHub-Warder-Evolution", "Unrelated-Warder-Evolution"),
    ("auxiliary-hybrid-runtime-candidate-2026-10-07", "other-candidate"),
    (sync.AUXILIARY_CANDIDATE_MANIFEST_ARCHIVE_REF, "warder-master-production"),
    (candidate_metadata_url, main_url),
)
for old, new in bad_url_replacements:
    bad_candidate = json.loads(json.dumps(candidate))
    current = bad_candidate["assets"]["piconProv-warder-safe-b"]["url"]
    bad_candidate["assets"]["piconProv-warder-safe-b"]["url"] = current.replace(old, new)
    assert sync.validate_auxiliary_candidate_manifest(bad_candidate, sync.AUXILIARY_CANDIDATE_MANIFEST_URL), (old, new)

# Wrong per-asset source, pin, size, root or pairing fails before job execution.
bad_catalog = json.loads(json.dumps(catalog))
bad_catalog["assets"]["piconProv-warder-safe-b"]["url"] = main_url
assert sync.validate_auxiliary_hybrid_catalog(bad_catalog, candidate)
bad_catalog = json.loads(json.dumps(catalog))
bad_catalog["assets"]["piconProv-warder-safe-b"]["sha256"] = "0" * 64
assert sync.validate_auxiliary_hybrid_catalog(bad_catalog, candidate)
bad_catalog = json.loads(json.dumps(catalog))
bad_catalog["auxiliary_hybrid"]["domains"]["provider"]["variants"]["black"]["install_order"] = ["warder_safe_priority", "legacy_fallback"]
assert sync.validate_auxiliary_hybrid_catalog(bad_catalog, candidate)

def validate_payload(payload, asset):
    with tempfile.NamedTemporaryFile(prefix="warder-aux-test-", suffix=".zip", delete=False) as f:
        f.write(payload)
        path = f.name
    try:
        return sync.validate_auxiliary_archive(path, asset)
    finally:
        os.unlink(path)

def zip_bytes(name, payload):
    import io
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(name, payload)
    return out.getvalue()

png = b"\x89PNG\r\n\x1a\n" + b"test-png-payload"
valid_zip = zip_bytes("piconProv/TEST.png", png)
asset = {"size": len(valid_zip), "sha256": hashlib.sha256(valid_zip).hexdigest(), "root": "piconProv", "png_count": 1}
assert validate_payload(valid_zip, asset) == []
assert "size mismatch" in " ".join(validate_payload(valid_zip, dict(asset, size=len(valid_zip) + 1)))
assert "SHA-256 mismatch" in " ".join(validate_payload(valid_zip, dict(asset, sha256="0" * 64)))
html = b"<html>not a zip</html>"
assert "not a ZIP" in " ".join(validate_payload(html, {"size":len(html),"sha256":hashlib.sha256(html).hexdigest(),"root":"piconProv","png_count":1}))
bad_zip = b"PK\x03\x04broken"
assert validate_payload(bad_zip, {"size":len(bad_zip),"sha256":hashlib.sha256(bad_zip).hexdigest(),"root":"piconProv","png_count":1})
traversal = zip_bytes("piconProv/../escape.png", png)
assert "unsafe auxiliary ZIP path" in " ".join(validate_payload(traversal, {"size":len(traversal),"sha256":hashlib.sha256(traversal).hexdigest(),"root":"piconProv","png_count":1}))
wrong_root = zip_bytes("piconSat/TEST.png", png)
assert "root/member mismatch" in " ".join(validate_payload(wrong_root, {"size":len(wrong_root),"sha256":hashlib.sha256(wrong_root).hexdigest(),"root":"piconProv","png_count":1}))

# Optional real archive fixtures can be supplied by a network/preflight run.
archive_dir = os.environ.get("WARDER_AUX_ARCHIVE_DIR")
if archive_dir:
    for asset_id, pin in sync.AUXILIARY_CANDIDATE_ASSETS.items():
        filename, size, sha, root, count = pin
        archive_path = Path(archive_dir) / filename
        assert archive_path.is_file(), archive_path
        asset = {"filename": filename, "size": size, "sha256": sha, "root": root, "png_count": count}
        assert sync.validate_auxiliary_archive(str(archive_path), asset) == [], asset_id
        with zipfile.ZipFile(str(archive_path), "r") as package:
            for item in package.infolist():
                if item.is_dir():
                    continue
                data = package.read(item)[:24]
                assert data.startswith(b"\x89PNG\r\n\x1a\n"), item.filename
                assert struct.unpack(">II", data[16:24]) == (220, 132), item.filename

with PLUGIN_PATH.open(encoding="utf-8") as f:
    plugin = f.read()
assert 'self._warderStartAuxiliaryComposite(self.menuListAll[x][0], self.type_download)' in plugin
assert 'self.warderAuxWorker.execute(sys.executable, sys.executable, worker_path, request_path, result_path)' in plugin
assert 'def _warderAuxWorkerClosed(self, exit_code):' in plugin
worker_text = (PLUGIN_DIR / "warderAuxiliaryWorker.py").read_text(encoding="utf-8")
assert "sync.build_auxiliary_jobs" in worker_text
assert "sync.build_production_auxiliary_jobs" in worker_text
assert "_run_job(fallback_job, base)" in worker_text and "_run_job(safe_job, base)" in worker_text
assert "_warderRunAuxiliaryComposite" not in plugin
assert "piconProv_220x132" in plugin and "piconSat_220x132" in plugin

# Exercise the actual GUI callback methods without importing Enigma2. The tests
# use only temporary result files and never invoke the worker or touch picons.
plugin_tree = ast.parse(plugin)
callback_nodes = {
    node.name: node for node in ast.walk(plugin_tree)
    if isinstance(node, ast.FunctionDef)
    and node.name in ("_warderAuxWorkerClosed", "_warderAuxWorkerOutputText",
                      "_warderAuxWorkerFailureText")
}
assert set(callback_nodes) == {
    "_warderAuxWorkerClosed", "_warderAuxWorkerOutputText",
    "_warderAuxWorkerFailureText",
}
callback_ns = {
    "json": json,
    "os": os,
    "_": lambda value: value,
    "warderPiconSync": SimpleNamespace(
        auxiliary_result_summary=lambda *args: {"text": "auxiliary result"}),
    "_warderRefreshInstalledAuxiliaryPicons": lambda: None,
}
callback_module = ast.Module(body=list(callback_nodes.values()), type_ignores=[])
exec(compile(ast.fix_missing_locations(callback_module), str(PLUGIN_PATH), "exec"), callback_ns)

class CallbackScreen:
    def __init__(self, result_path, output):
        self.warderAuxResultPath = result_path
        self.warderAuxRequestPath = None
        self.warderAuxWorker = None
        self.warderAuxWorkerRunning = True
        self.warderAuxOutput = output
        self.messages = []

    def _warderAuxWorkerCleanup(self):
        for path in (self.warderAuxRequestPath, self.warderAuxResultPath):
            if path:
                try:
                    os.unlink(path)
                except OSError:
                    pass
        self.warderAuxRequestPath = None
        self.warderAuxResultPath = None
        self.warderAuxWorker = None

    def dwnLoop(self, message):
        self.messages.append(message)

for case, payload, exit_status, output, expected in (
    ("missing", None, 127, "worker failed to start", "missing or unsafe"),
    ("empty", b"", 1, "ModuleNotFoundError: test", "result file is empty"),
    ("malformed", b"{", 1, "worker stderr", "invalid auxiliary worker result JSON"),
    ("fatal", json.dumps({"fatal_error": "manifest parse failed", "results": []}).encode(), 1,
     "worker stderr", "manifest parse failed"),
):
    with tempfile.TemporaryDirectory(prefix="warder-aux-callback-test-") as temp:
        result_path = os.path.join(temp, "result.json")
        if payload is not None:
            with open(result_path, "wb") as stream:
                stream.write(payload)
        screen = CallbackScreen(result_path, [output])
        screen._warderAuxWorkerOutputText = MethodType(
            callback_ns["_warderAuxWorkerOutputText"], screen)
        screen._warderAuxWorkerFailureText = MethodType(
            callback_ns["_warderAuxWorkerFailureText"], screen)
        screen._warderAuxWorkerClosed = MethodType(
            callback_ns["_warderAuxWorkerClosed"], screen)
        screen._warderAuxWorkerClosed(exit_status)
        message = screen.messages[-1]
        assert expected in message, (case, message)
        assert "Worker exit status: %d" % exit_status in message, (case, message)
        assert output in message, (case, message)
        assert "Expecting value: line 1 column 1 (char 0)" not in message, (case, message)

with tempfile.TemporaryDirectory(prefix="warder-aux-callback-test-") as temp:
    result_path = os.path.join(temp, "result.json")
    with open(result_path, "w", encoding="utf-8") as stream:
        json.dump({"kind": "provider", "variant": "black", "results": []}, stream)
    screen = CallbackScreen(result_path, [])
    screen._warderAuxWorkerOutputText = MethodType(callback_ns["_warderAuxWorkerOutputText"], screen)
    screen._warderAuxWorkerFailureText = MethodType(callback_ns["_warderAuxWorkerFailureText"], screen)
    screen._warderAuxWorkerClosed = MethodType(callback_ns["_warderAuxWorkerClosed"], screen)
    screen._warderAuxWorkerClosed(0)
    assert screen.messages == ["auxiliary result"], screen.messages


# All 19 supported catalogs carry the user-facing task text and compile-ready translations.
locale_root = PLUGIN_DIR / "locale"
required = ("Close", "220 x 132 - Picons", "PATHS", "Transparent", "Black", "White",
            "Provider logos", "Satellite logos", "Fallback %d/%d; safe overlay %d/%d; errors %d")
catalogs = sorted(locale_root.glob("*/LC_MESSAGES/setupGlass17.po"))
assert len(catalogs) == 19, len(catalogs)
for po in catalogs:
    text = po.read_text(encoding="utf-8")
    for msgid in required:
        match = re.search(r'(?m)^msgid "' + re.escape(msgid) + r'"\r?\nmsgstr "([^"\r\n]*)"', text)
        assert match and match.group(1), (po.parent.parent.name, msgid)
sk = (locale_root / "sk/LC_MESSAGES/setupGlass17.po").read_text(encoding="utf-8")
assert 'msgid "PATHS"\nmsgstr "CESTY KU KONFIGURAČNÝM SÚBOROM SKINU"' in sk
assert 'msgid "220 x 132 - Picons"\nmsgstr "220 × 132 – Picony"' in sk
icon_path = ROOT / "source/package-root/usr/share/enigma2/hd_glass17/down/warder-colour.png"
icon_header = icon_path.read_bytes()[:26]
assert icon_header.startswith(b"\x89PNG\r\n\x1a\n")
assert struct.unpack(">II", icon_header[16:24]) == (189, 123)
assert icon_header[25] == 6

# A successful layer plus a failed layer must be partial/red, never green.
result = sync.auxiliary_result_summary("provider", "black", 1297, 1297, 0, 172)
assert result["status"] == "PARTIAL SUCCESS" and result["failures"] == 172
result = sync.auxiliary_result_summary("provider", "black", 0, 1297, 0, 172)
assert result["status"] == "ERROR" and result["updated"] == 0

# Preserve the recorded TEST201 receiver baseline in the result-count contract.
baseline = sync.package_result_summary([
    {"orbital_position": "13.0E", "package_selector": "130E", "updated": 1021, "failures": 0},
    {"orbital_position": "16.0E", "package_selector": "160E", "updated": 459, "failures": 0},
    {"orbital_position": "19.2E", "package_selector": "192E", "updated": 622, "failures": 0},
    {"orbital_position": "23.5E", "package_selector": "235E", "updated": 541, "failures": 0},
])
assert baseline["status"] == "SUCCESSFUL"
assert "Total: 2643 picons updated" in baseline["text"]
assert "Failures: 0" in baseline["text"]
assert all(position in baseline["text"] for position in ("13.0E", "16.0E", "19.2E", "23.5E"))

print("PASS: hybrid publication/runtime plus auxiliary GUI missing/empty/malformed/fatal/success result handling")
