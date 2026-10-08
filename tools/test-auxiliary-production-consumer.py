#!/usr/bin/env python3
"""Offline integrity and receiver-boundary regressions for production aux catalog."""
import gzip
import ast
import hashlib
import importlib.util
import json
import os
import shutil
import tempfile
import zipfile
import stat
import struct
import sys
import weakref
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
SYNC_PATH = PLUGIN_DIR / "warderPiconSync.py"
spec = importlib.util.spec_from_file_location("warder_aux_production_test", str(SYNC_PATH))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

descriptor_raw = (PLUGIN_DIR / "auxiliaryProduction.json").read_bytes()
descriptor = json.loads(descriptor_raw.decode("utf-8"))
catalog_raw = (ROOT / "tools/fixtures/auxiliary-production-catalog-4e0e7233.json.gz").read_bytes()
catalog_raw = gzip.decompress(catalog_raw)
catalog = json.loads(catalog_raw.decode("utf-8"))
assert sync.validate_auxiliary_production_descriptor(descriptor, descriptor_raw) == []
assert sync.trusted_auxiliary_production_manifest_url(descriptor["catalog"]["url"])
assert not sync.trusted_auxiliary_production_manifest_url(descriptor["catalog"]["url"].replace(sync.AUXILIARY_PRODUCTION_COMMIT, "0" * 40))
assert sync.validate_auxiliary_production_catalog(catalog, catalog_raw, descriptor) == []
assert hashlib.sha256(catalog_raw).hexdigest() == descriptor["catalog"]["sha256"]

# The descriptor fails closed on a source commit, archive pin, or content contract change.
for mutate in (
    lambda d: d["catalog"].update(commit="0" * 40),
    lambda d: d["archive_bundle"].update(commit="warder-master-production"),
    lambda d: d["archive_bundle"]["assets"]["provider-black"].update(sha256="0" * 64),
    lambda d: d["archive_bundle"]["assets"]["provider-black"].update(size=1),
    lambda d: d["archive_bundle"]["assets"]["satellite-white"].update(png_count=2),
    lambda d: d["archive_bundle"]["assets"]["provider-white"].update(root="picons/23.5e"),
):
    bad = json.loads(json.dumps(descriptor))
    mutate(bad)
    assert sync.validate_auxiliary_production_descriptor(bad)
assert sync.validate_auxiliary_production_descriptor(descriptor, descriptor_raw + b" ")

# Catalog requires unique namespaced IDs, complete B/W pairs and exact domain paths.
for mutate in (
    lambda d: d["entries"][1].update(identity=d["entries"][0]["identity"]),
    lambda d: d["entries"][0].update(kind="satellite-logo"),
    lambda d: d["entries"][0].update(black={"path": "auxiliary/provider-logo/black/../escape.png", "sha256": "0" * 64}),
    lambda d: d["entries"][0].update(white=None),
):
    bad = json.loads(json.dumps(catalog))
    mutate(bad)
    assert sync.validate_auxiliary_production_catalog(bad, catalog_raw, descriptor)
assert sync.validate_auxiliary_production_catalog(catalog, catalog_raw + b" ", descriptor)


def make_png(width=220, height=132, color_type=6):
    return (b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR"
            + struct.pack(">II", width, height) + bytes((8, color_type, 0, 0, 0)) + b"0000")


def make_archive(member_name, payload, symlink=False):
    import io
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as package:
        info = zipfile.ZipInfo(member_name)
        if symlink:
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
        package.writestr(info, payload)
    return out.getvalue()


def archive_errors(payload, member_map=None, count=1):
    with tempfile.NamedTemporaryFile(prefix="warder-aux-guard-", suffix=".zip", delete=False) as stream:
        stream.write(payload)
        path = stream.name
    try:
        asset = {"size": len(payload), "sha256": hashlib.sha256(payload).hexdigest(),
                 "root": "piconProv_220x132", "png_count": count}
        if member_map is not None:
            asset.update({"member_sha256": member_map, "dimensions": [220, 132], "mode": "RGBA"})
        return sync.validate_auxiliary_archive(path, asset)
    finally:
        os.unlink(path)


sample_png = make_png()
assert not archive_errors(make_archive("piconProv_220x132/SAFE.png", sample_png), {"SAFE.png": hashlib.sha256(sample_png).hexdigest()})
assert archive_errors(make_archive("piconProv_220x132/../escape.png", sample_png))
assert archive_errors(make_archive("piconProv_220x132/link.png", b"SAFE.png", symlink=True))
assert archive_errors(make_archive("piconProv_220x132/unexpected.txt", sample_png))
assert archive_errors(make_archive("piconProv_220x132/SAFE.png", sample_png), {"SAFE.png": "0" * 64})
assert archive_errors(make_archive("piconProv_220x132/SAFE.png", make_png(219, 132)),
                      {"SAFE.png": hashlib.sha256(make_png(219, 132)).hexdigest()})

provider_entries = [e for e in catalog["entries"] if e["kind"] == "provider-logo"]
satellite_entries = [e for e in catalog["entries"] if e["kind"] == "satellite-logo"]
assert len(provider_entries) == 172 and len(satellite_entries) == 1
assert len(set(e["identity"] for e in catalog["entries"])) == 173
assert len(set(e[v]["path"] for e in catalog["entries"] for v in ("black", "white"))) == 346
assert all(e["qc_status"] == "PASS" for e in catalog["entries"])
assert "BOUNDED_AA_V1" in next(e for e in catalog["entries"] if e["filename"] == "ODESA LAYV.png")["visual_approval_provenance"]

archive_root = ROOT / "assets/warder/downloads/picons/auxiliary-staging-production"
for kind, variant, filename, count in (
    ("provider", "black", "provider-black.zip", 172),
    ("provider", "white", "provider-white.zip", 172),
    ("satellite", "black", "satellite-black.zip", 1),
    ("satellite", "white", "satellite-white.zip", 1),
):
    plan = sync.build_production_auxiliary_jobs(catalog, descriptor, kind, variant)
    assert plan["state"] == "ready" and len(plan["jobs"]) == 1
    job = plan["jobs"][0]
    archive = archive_root / filename
    assert archive.stat().st_size == job["size"]
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == job["sha256"]
    assert job["png_count"] == count and len(job["member_sha256"]) == count
    assert sync.validate_auxiliary_archive(str(archive), job) == []
    with zipfile.ZipFile(str(archive), "r") as package:
        assert len([x for x in package.infolist() if not x.is_dir()]) == count

# Exact namespaced lookup is auxiliary-only; unknown/cross-domain IDs miss.
for entry in catalog["entries"]:
    for variant in ("black", "white"):
        item = sync.lookup_auxiliary(catalog, entry["kind"], entry["filename"], variant)
        assert item and item["sha256"] == entry[variant]["sha256"]
assert sync.lookup_auxiliary(catalog, "provider-logo", "NO SUCH PROVIDER.png", "black") is None
assert sync.lookup_auxiliary(catalog, "provider-logo", "150W.png", "black") is None
assert sync.lookup_auxiliary(catalog, "satellite-logo", "150W.png", "black") is None if satellite_entries[0]["filename"] != "150W.png" else True
assert sync.lookup_auxiliary(catalog, "satellite-logo", "150.0W.png", "black") is None
assert sync.lookup_auxiliary(catalog, "provider-logo", "../150W.png", "black") is None
assert sync.lookup_auxiliary(catalog, "satellite-logo", satellite_entries[0]["filename"], "black")
assert sync.auxiliary_identity_key("satellite-logo", satellite_entries[0]["filename"]).startswith("satellite-logo::")
assert sync.auxiliary_comma_compatibility_filename("DB MUX 4") == "DB, MUX 4.png"
assert sync.auxiliary_comma_compatibility_filename("DB PPRECHOD. MUX 13") == "DB, PPRECHOD. MUX 13.png"
assert sync.auxiliary_comma_compatibility_filename("UNRELATED, PROVIDER") is None
sid_names = [e["filename"] for e in provider_entries if e["filename"].startswith("SID ")]
assert len(sid_names) == 21
assert not any(sync.auxiliary_comma_compatibility_filename(e[:-4]) for e in sid_names)
def current_fix_name(value):
    value = "".join(char for char in value if ord(char) < 128)
    return value.replace("\t", "").strip().upper().replace(",", "").replace("(", "").replace(")", "")
provider_normalized = {}
for entry in provider_entries:
    provider_normalized.setdefault(current_fix_name(entry["filename"][:-4]), []).append(entry["filename"])
assert not [names for names in provider_normalized.values() if len(names) > 1]
assert [name for name in (e["filename"] for e in provider_entries)
        if current_fix_name(name[:-4]) != name[:-4]] == ["DB, MUX 4.png", "DB, PPRECHOD. MUX 13.png"]

# Existing fallback pins and lookup priority remain. Transparent jobs still use the old hybrid path.
downloads = json.loads((ROOT / "assets/warder/downloads.json").read_text(encoding="utf-8"))
for kind in ("provider", "satellite"):
    for variant in ("black", "white"):
        plan = sync.build_legacy_fallback_job(downloads, kind, variant)
        assert plan["state"] == "ready" and plan["jobs"][0]["root"] in ("piconProv", "piconSat")
    for variant in ("transparent", "black", "white"):
        assert (variant, variant.title()) in sync.auxiliary_hybrid_variants("piconProv" if kind == "provider" else "piconSat")
assert sync.auxiliary_hybrid_variants("piconProv")[0][0] == "transparent"
assert sync.build_auxiliary_rollback_job(descriptor, "provider", "black")["jobs"][0]["destination"] == "piconProv_220x132"
assert sync.build_auxiliary_rollback_job(descriptor, "satellite", "white")["jobs"][0]["destination"] == "piconSat_220x132"

# Install a real pinned satellite overlay in a temporary receiver-like tree. Base and unrelated files survive.
with tempfile.TemporaryDirectory(prefix="warder-aux-install-test-") as temp:
    base = Path(temp)
    base.mkdir(exist_ok=True)
    safe_dir = base / "piconSat_220x132"
    safe_dir.mkdir()
    (safe_dir / "unrelated.txt").write_text("keep", encoding="ascii")
    old_file = safe_dir / satellite_entries[0]["filename"]
    old_file.write_bytes(b"old-current")
    (base / "piconSat").mkdir()
    (base / "piconSat" / "legacy.png").write_bytes(b"legacy")
    job = sync.build_production_auxiliary_jobs(catalog, descriptor, "satellite", "black")["jobs"][0]
    installed = sync.install_auxiliary_archive(str(archive_root / "satellite-black.zip"), job, str(safe_dir))
    assert installed == {"updated": 1, "attempted": 1, "error": ""}
    assert hashlib.sha256(old_file.read_bytes()).hexdigest() == job["member_sha256"][satellite_entries[0]["filename"]]
    assert (safe_dir / "unrelated.txt").read_text(encoding="ascii") == "keep"
    assert (base / "piconSat" / "legacy.png").read_bytes() == b"legacy"
    before = old_file.read_bytes()
    bad = dict(job, sha256="0" * 64)
    failed = sync.install_auxiliary_archive(str(archive_root / "satellite-black.zip"), bad, str(safe_dir))
    assert failed["updated"] == 0 and old_file.read_bytes() == before

# GUI only starts a queued subprocess; network/archive work is isolated in the worker module.
plugin = (PLUGIN_DIR / "plugin.py").read_text(encoding="utf-8")
worker = (PLUGIN_DIR / "warderAuxiliaryWorker.py").read_text(encoding="utf-8")
assert "self._warderStartAuxiliaryComposite(self.menuListAll[x][0], self.type_download)" in plugin
assert "self.warderAuxWorker.execute(sys.executable, worker_path, request_path, result_path)" in plugin
assert "urlopen(" not in plugin[plugin.index("def _warderStartAuxiliaryComposite"):plugin.index("def _warderRemoveStaleChannelPicons")]
assert "_run_job(fallback_job, base)" in worker and "_run_job(safe_job, base)" in worker
assert "_warderRunAuxiliaryComposite" not in plugin
assert 'pngname = self.findPicon(what)' in plugin and 'picon_sat.png' in plugin
assert "piconProv_220x132" in plugin and "piconSat_220x132" in plugin
provider_block = plugin[plugin.index("compatibility_name = warderPiconSync.auxiliary_comma_compatibility_filename(sname)"):plugin.index('sname = "picon_default"', plugin.index("compatibility_name = warderPiconSync.auxiliary_comma_compatibility_filename(sname)"))]
assert provider_block.index("priority_path") < provider_block.index("self.findPicon(sname)") < provider_block.index("self.findPicon(compatibility_name[:-4])")
assert "remove(" not in worker and "unlink(" in worker  # only temporary/archive rollback files are unlinked

# A successful overlay refreshes the current exact tokens even when they did
# not change. A failed or partial safe layer must not call the refresh gate.
plugin_ast = ast.parse(plugin, filename="plugin.py")
registry_defs = [node for node in plugin_ast.body if isinstance(node, ast.FunctionDef)
                 and node.name in ("_warderRegisterAuxiliaryPiconConsumer",
                                   "_warderRefreshInstalledAuxiliaryPicons")]
registry_ns = {"weakref": weakref, "_WARDER_AUX_PICON_CONSUMERS": []}
exec(compile(ast.Module(body=registry_defs, type_ignores=[]), "plugin-refresh-regression", "exec"), registry_ns)

class _CurrentTokenConsumer:
    def __init__(self):
        self.provider_token = "DB MUX 4"
        self.satellite_token = "150W"
        self.refresh_count = 0
        self.tokens_seen = None

    def _warderRefreshAuxiliaryPicons(self):
        self.refresh_count += 1
        self.tokens_seen = (self.provider_token, self.satellite_token)

consumer = _CurrentTokenConsumer()
registry_ns["_warderRegisterAuxiliaryPiconConsumer"](consumer)
registry_ns["_warderRefreshInstalledAuxiliaryPicons"]()
assert consumer.refresh_count == 1 and consumer.tokens_seen == ("DB MUX 4", "150W")
worker_closed = next(node for node in ast.walk(plugin_ast)
                     if isinstance(node, ast.FunctionDef) and node.name == "_warderAuxWorkerClosed")
refresh_gate = next(node.test for node in ast.walk(worker_closed)
                    if isinstance(node, ast.If)
                    and any(isinstance(child, ast.Call) and isinstance(child.func, ast.Name)
                            and child.func.id == "_warderRefreshInstalledAuxiliaryPicons"
                            for stmt in node.body for child in ast.walk(stmt)))
refresh_allowed = compile(ast.Expression(refresh_gate), "plugin-refresh-gate", "eval")
assert eval(refresh_allowed, {"safe_total": 172, "safe": {"updated": 172, "error": ""}})
assert not eval(refresh_allowed, {"safe_total": 172, "safe": {"updated": 0, "error": "copy failed"}})
assert not eval(refresh_allowed, {"safe_total": 172, "safe": {"updated": 172, "error": "copy failed"}})

# Exercise the actual worker end-to-end using committed manifests and ZIPs, with
# URL responses mapped locally so the test remains deterministic and offline.
worker_spec = importlib.util.spec_from_file_location("warder_aux_worker_test", PLUGIN_DIR / "warderAuxiliaryWorker.py")
worker_module = importlib.util.module_from_spec(worker_spec)
sys.path.insert(0, str(PLUGIN_DIR))
worker_spec.loader.exec_module(worker_module)
downloads_url = "https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/warder-modernization-work/assets/warder/downloads.json"
downloads = json.loads((ROOT / "assets/warder/downloads.json").read_text(encoding="utf-8"))
url_payloads = {downloads_url: (ROOT / "assets/warder/downloads.json").read_bytes()}
for asset_id, item in downloads["assets"].items():
    if asset_id in ("piconProv-b", "piconProv-w", "piconSat-b", "piconSat-w"):
        local = ROOT / "assets/warder/downloads" / item["url"].split("/assets/warder/downloads/", 1)[1]
        url_payloads[item["url"]] = local.read_bytes()
url_payloads[descriptor["catalog"]["url"]] = catalog_raw
for item in descriptor["archive_bundle"]["assets"].values():
    url_payloads[item["url"]] = (archive_root / item["filename"]).read_bytes()


class Response:
    def __init__(self, url, payload):
        self._url = url
        self._payload = payload
        self._offset = 0
        self.headers = {"Content-Type": "text/plain" if url.endswith((".json", "downloads.json")) else "application/zip"}

    def geturl(self):
        return self._url

    def read(self, amount=-1):
        if amount < 0:
            amount = len(self._payload) - self._offset
        value = self._payload[self._offset:self._offset + amount]
        self._offset += len(value)
        return value

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False


old_urlopen = worker_module.urlopen
worker_module.urlopen = lambda request, timeout=45: Response(request.full_url, url_payloads[request.full_url])
try:
    with tempfile.TemporaryDirectory(prefix="warder-aux-worker-e2e-") as temp:
        provider_result = worker_module.run({"row": "aux-prov", "variant": "black", "destination_base": temp,
            "downloads_manifest_url": downloads_url, "descriptor_path": str(PLUGIN_DIR / "auxiliaryProduction.json")})
        layers = {item["layer"]: item["result"] for item in provider_result["results"]}
        assert layers["legacy_fallback"]["updated"] == layers["legacy_fallback"]["attempted"] == 1297, layers
        assert layers["warder_safe_priority"]["updated"] == layers["warder_safe_priority"]["attempted"] == 172, layers
        assert len(list((Path(temp) / "piconProv").glob("*.png"))) == 1297
        assert len(list((Path(temp) / "piconProv_220x132").glob("*.png"))) == 172
        satellite_result = worker_module.run({"row": "aux-sat", "variant": "white", "destination_base": temp,
            "downloads_manifest_url": downloads_url, "descriptor_path": str(PLUGIN_DIR / "auxiliaryProduction.json")})
        satellite_layers = {item["layer"]: item["result"] for item in satellite_result["results"]}
        assert satellite_layers["legacy_fallback"]["updated"] == satellite_layers["legacy_fallback"]["attempted"] == 269
        assert satellite_layers["warder_safe_priority"]["updated"] == satellite_layers["warder_safe_priority"]["attempted"] == 1
finally:
    worker_module.urlopen = old_urlopen

print("PASS: 173 identities; 346 exact PNG pins; descriptor/catalog; lookup; safe install; fallback; rollback; async boundary")
