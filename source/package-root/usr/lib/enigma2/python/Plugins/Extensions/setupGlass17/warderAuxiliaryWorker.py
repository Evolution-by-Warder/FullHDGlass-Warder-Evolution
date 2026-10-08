# -*- coding: utf-8 -*-
"""Standard-library worker for non-blocking Provider/Satellite installs."""
from __future__ import absolute_import

import hashlib
import json
import os
import sys
import tempfile

try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen

import warderPiconSync as sync

USER_AGENT = "FullHDGlass17-Warder-Evolution/auxiliary-picons"


def _fetch_bytes(url, source_id, maximum, content_types=None):
    if source_id == "piconhub-aux-production-manifest":
        if not sync.trusted_auxiliary_production_manifest_url(url):
            raise ValueError("untrusted auxiliary production catalog URL")
    elif source_id == "fullhd-runtime-downloads":
        if not sync.trusted_auxiliary_runtime_downloads_url(url):
            raise ValueError("untrusted FullHD downloads manifest URL")
    elif source_id == "piconhub-aux-candidate-manifest":
        if url != sync.AUXILIARY_CANDIDATE_MANIFEST_URL:
            raise ValueError("untrusted existing transparent candidate manifest")
    elif not sync.trusted_auxiliary_url(url, source_id):
        raise ValueError("untrusted auxiliary source URL")
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json, application/zip, application/octet-stream"})
    with urlopen(request, timeout=45) as response:
        final_url = str(response.geturl())
        if source_id in ("piconhub-aux-production-manifest", "fullhd-runtime-downloads"):
            if final_url != url:
                raise ValueError("unsafe downloads manifest redirect")
            allowed = content_types or ("application/json", "text/plain", "application/octet-stream")
            content_type = str(response.headers.get("Content-Type", "")).split(";", 1)[0].strip().lower()
            if content_type not in allowed:
                raise ValueError("unexpected downloads manifest content type")
        elif source_id == "piconhub-aux-candidate-manifest":
            if final_url != url:
                raise ValueError("unsafe existing transparent manifest redirect")
        elif not sync.trusted_auxiliary_url(final_url, source_id):
            raise ValueError("unsafe auxiliary redirect")
        if source_id == "fullhd-aux-production-bundle":
            allowed = content_types or ("application/zip", "application/octet-stream", "text/plain")
            content_type = str(response.headers.get("Content-Type", "")).split(";", 1)[0].strip().lower()
            if content_type not in allowed:
                raise ValueError("unexpected auxiliary archive content type")
        data = response.read(maximum + 1)
        if len(data) > maximum:
            raise ValueError("oversized auxiliary response")
        if data.lstrip().lower().startswith((b"<html", b"<!doctype")):
            raise ValueError("auxiliary source returned HTML")
        return data


def _download_archive(job, directory):
    expected_size = int(job.get("size", 0))
    if expected_size < 1 or expected_size > 32 * 1024 * 1024:
        raise ValueError("invalid auxiliary archive size")
    url = str(job.get("url", ""))
    source_id = job.get("publication_source_id")
    if not sync.trusted_auxiliary_url(url, source_id):
        raise ValueError("unsafe auxiliary archive URL")
    fd, path = tempfile.mkstemp(prefix="warder-aux-", suffix=".zip", dir=directory)
    try:
        digest = hashlib.sha256()
        total = 0
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/zip, application/octet-stream"})
        with urlopen(request, timeout=45) as response:
            if not sync.trusted_auxiliary_url(str(response.geturl()), source_id):
                raise ValueError("unsafe auxiliary archive redirect")
            if source_id == "fullhd-aux-production-bundle":
                content_type = str(response.headers.get("Content-Type", "")).split(";", 1)[0].strip().lower()
                if content_type not in job.get("allowed_content_types", []):
                    raise ValueError("unexpected auxiliary archive content type")
            stream = os.fdopen(fd, "wb")
            with stream:
                while True:
                    chunk = response.read(128 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > expected_size:
                        raise ValueError("oversized auxiliary archive")
                    digest.update(chunk)
                    stream.write(chunk)
                stream.flush()
                os.fsync(stream.fileno())
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.unlink(path)
        except OSError:
            pass
        raise
    if total != expected_size:
        os.unlink(path)
        raise ValueError("auxiliary archive size mismatch")
    if digest.hexdigest() != str(job.get("sha256", "")):
        os.unlink(path)
        raise ValueError("auxiliary archive SHA-256 mismatch")
    errors = sync.validate_auxiliary_archive(path, job)
    if errors:
        os.unlink(path)
        raise ValueError("invalid auxiliary archive: " + "; ".join(errors[:3]))
    return path


def _destination(base, root):
    if root not in ("piconProv", "piconProv_220x132", "piconSat", "piconSat_220x132"):
        raise ValueError("invalid auxiliary destination")
    if not os.path.isabs(base) or os.path.islink(base) or not os.path.isdir(base):
        raise ValueError("unsafe auxiliary base directory")
    base = os.path.realpath(base)
    target = os.path.join(base, root)
    if os.path.islink(target):
        raise ValueError("auxiliary destination is a symbolic link")
    if not os.path.exists(target):
        os.mkdir(target)
    if not os.path.isdir(target) or os.path.realpath(target) != target:
        raise ValueError("unsafe auxiliary destination")
    return target


def _run_job(job, base):
    archive = None
    try:
        archive = _download_archive(job, "/tmp")
        target = _destination(base, str(job.get("destination", job.get("root", ""))))
        return sync.install_auxiliary_archive(archive, job, target)
    except Exception as err:
        return {"updated": 0, "attempted": int(job.get("png_count", 0)), "error": str(err)}
    finally:
        if archive:
            try:
                os.unlink(archive)
            except OSError:
                pass


def _load_downloads(url):
    raw = _fetch_bytes(url, "fullhd-runtime-downloads", 4 * 1024 * 1024)
    doc = json.loads(raw.decode("utf-8"))
    if not isinstance(doc, dict) or not isinstance(doc.get("assets"), dict):
        raise ValueError("invalid FullHD auxiliary downloads manifest")
    return doc


def _load_old_candidate():
    desc = sync.AUXILIARY_PUBLICATION_SOURCES["piconhub-aux-candidate"]
    raw = _fetch_bytes(desc["manifest_url"], "piconhub-aux-candidate-manifest", 1024 * 1024)
    doc = json.loads(raw.decode("utf-8"))
    errors = sync.validate_auxiliary_candidate_manifest(doc, desc["manifest_url"])
    if errors:
        raise ValueError("invalid existing transparent auxiliary source: " + "; ".join(errors[:3]))
    return doc


def run(request):
    row = request.get("row")
    kind = {"aux-prov": "provider", "aux-sat": "satellite"}.get(row)
    variant = request.get("variant")
    base = request.get("destination_base")
    if kind is None or variant not in ("transparent", "black", "white"):
        raise ValueError("invalid auxiliary task")
    downloads_url = request.get("downloads_manifest_url")
    downloads = _load_downloads(downloads_url)
    results = []
    fallback_plan = sync.build_legacy_fallback_job(downloads, kind, variant) if variant != "transparent" else None
    if variant == "transparent":
        hybrid = downloads.get("auxiliary_hybrid")
        assets = dict(downloads.get("assets", {}))
        if not isinstance(hybrid, dict):
            raise ValueError("existing transparent auxiliary catalog missing")
        candidate = None
        candidate_error = None
        try:
            candidate = _load_old_candidate()
        except Exception as err:
            candidate_error = str(err)
        plan = sync.build_auxiliary_jobs({"assets": assets, "auxiliary_hybrid": hybrid}, candidate, kind, variant)
        if plan.get("state") != "ready" or len(plan.get("jobs", [])) != 2:
            raise ValueError("existing transparent auxiliary plan rejected")
        fallback_job, safe_job = plan["jobs"]
        results.append({"layer": fallback_job["layer"], "asset_id": fallback_job["asset_id"],
                        "result": _run_job(fallback_job, base)})
        if candidate_error:
            safe_result = {"updated": 0, "attempted": int(safe_job.get("png_count", 0)), "error": candidate_error}
        else:
            safe_result = _run_job(safe_job, base)
        results.append({"layer": safe_job["layer"], "asset_id": safe_job["asset_id"], "result": safe_result})
    else:
        if fallback_plan.get("state") != "ready":
            raise ValueError("legacy fallback plan rejected: " + "; ".join(fallback_plan.get("errors", [])))
        fallback_job = fallback_plan["jobs"][0]
        results.append({"layer": fallback_job["layer"], "asset_id": fallback_job["asset_id"],
                        "result": _run_job(fallback_job, base)})
        safe_result = None
        safe_job = None
        expected_count = 172 if kind == "provider" else 1
        try:
            descriptor_path = request.get("descriptor_path")
            descriptor, descriptor_errors = sync.load_auxiliary_production_descriptor(descriptor_path)
            if descriptor_errors:
                raise ValueError("auxiliary production descriptor rejected: " + "; ".join(descriptor_errors[:3]))
            catalog_pin = descriptor["catalog"]
            raw = _fetch_bytes(catalog_pin["url"], "piconhub-aux-production-manifest", catalog_pin["size"],
                               tuple(catalog_pin.get("allowed_content_types", [])))
            document = json.loads(raw.decode("utf-8"))
            errors = sync.validate_auxiliary_production_catalog(document, raw, descriptor)
            if errors:
                raise ValueError("auxiliary production catalog rejected: " + "; ".join(errors[:3]))
            safe_plan = sync.build_production_auxiliary_jobs(document, descriptor, kind, variant)
            if safe_plan.get("state") != "ready" or len(safe_plan.get("jobs", [])) != 1:
                raise ValueError("auxiliary production archive plan rejected")
            safe_job = safe_plan["jobs"][0]
            safe_result = _run_job(safe_job, base)
            expected_count = int(safe_job.get("png_count", expected_count))
        except Exception as err:
            safe_result = {"updated": 0, "attempted": expected_count, "error": str(err)}
        results.append({"layer": "warder_safe_priority", "asset_id": (safe_job or {}).get("asset_id", "production-safe-overlay"),
                        "result": safe_result})
    return {"row": row, "kind": kind, "variant": variant, "results": results}


def main(argv):
    if len(argv) != 3:
        return 2
    request_path, result_path = argv[1], argv[2]
    try:
        if os.path.islink(request_path) or not os.path.isfile(request_path):
            raise ValueError("invalid worker request file")
        with open(request_path, "rb") as stream:
            raw = stream.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise ValueError("worker request too large")
        result = run(json.loads(raw.decode("utf-8")))
        code = 0
    except Exception as err:
        result = {"row": "", "results": [], "fatal_error": str(err)}
        code = 1
    temp_path = result_path + ".new"
    with open(temp_path, "w") as stream:
        json.dump(result, stream, sort_keys=True, separators=(",", ":"))
        stream.flush()
        os.fsync(stream.fileno())
    os.rename(temp_path, result_path)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
