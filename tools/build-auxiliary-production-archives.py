#!/usr/bin/env python3
"""Build deterministic receiver ZIPs from the immutable PiconHub auxiliary catalog.

This is a staging publisher only. It never renders or modifies a source PNG.
The input checkout must be the exact approved PiconHub production commit.
"""
import argparse
import hashlib
import json
import os
import re
import stat
import struct
import zipfile

SOURCE_REPOSITORY = "Evolution-by-Warder/PiconHub-Warder-Evolution"
SOURCE_COMMIT = "4e0e7233e93d4fc6afc5b22447730b3e8e5eaefd"
MANIFEST_REL = "reports/auxiliary-production-integration-2026-10-08/auxiliary-catalog.json"
MANIFEST_SHA256 = "6631f646ed3d51a1e84317c9e3a45456b48c002781dc7338442e5c4d26b3a754"
EXPECTED_CANDIDATE = "8bf726a3d7ba046f5bc531c8236b573963b7557a"
# The production catalog's provenance string stores this exact historical
# value (one hex character shorter than the separately recorded QC checkpoint).
EXPECTED_QC_PROVENANCE = "13dd00b5624c4b6659574cdddedd503edc18947"
ARCHIVES = (
    ("provider-logo", "black", "provider-black.zip", "piconProv_220x132", 172),
    ("provider-logo", "white", "provider-white.zip", "piconProv_220x132", 172),
    ("satellite-logo", "black", "satellite-black.zip", "piconSat_220x132", 1),
    ("satellite-logo", "white", "satellite-white.zip", "piconSat_220x132", 1),
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def safe_filename(value):
    return (isinstance(value, str) and value == os.path.basename(value)
            and value.lower().endswith(".png") and value not in (".", "..")
            and "/" not in value and "\\" not in value and "\x00" not in value)


def load_verified_catalog(source_root):
    manifest_path = os.path.join(source_root, MANIFEST_REL)
    raw = open(manifest_path, "rb").read()
    if sha256_bytes(raw) != MANIFEST_SHA256:
        raise ValueError("PiconHub auxiliary manifest SHA256 mismatch")
    document = json.loads(raw.decode("utf-8"))
    if document.get("schema_version") != 1 or len(document.get("entries", [])) != 173:
        raise ValueError("unexpected PiconHub auxiliary catalog schema/count")
    seen = set()
    kinds = {"provider-logo": 0, "satellite-logo": 0}
    for entry in document["entries"]:
        kind = entry.get("kind")
        filename = entry.get("filename")
        identity = entry.get("identity")
        if kind not in kinds or not safe_filename(filename) or identity != kind + "::" + filename:
            raise ValueError("invalid auxiliary identity")
        if identity in seen or entry.get("qc_status") != "PASS":
            raise ValueError("duplicate or unapproved auxiliary identity")
        seen.add(identity)
        kinds[kind] += 1
        provenance = entry.get("visual_approval_provenance", "")
        if ("approved_candidate_checkpoint=" + EXPECTED_CANDIDATE not in provenance
                or "approved_qc_checkpoint=" + EXPECTED_QC_PROVENANCE not in provenance):
            raise ValueError("missing approved candidate/QC provenance")
        for variant in ("black", "white"):
            record = entry.get(variant)
            expected_path = "auxiliary/%s/%s/%s" % (kind, variant, filename)
            if (not isinstance(record, dict) or record.get("path") != expected_path
                    or not SHA256_RE.match(str(record.get("sha256", "")))):
                raise ValueError("invalid variant path/hash for " + identity)
    if kinds != {"provider-logo": 172, "satellite-logo": 1}:
        raise ValueError("unexpected auxiliary identity domain counts")
    return document


def png_is_220x132_rgba(path):
    with open(path, "rb") as stream:
        header = stream.read(29)
    if len(header) != 29 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return False
    width, height = struct.unpack(">II", header[16:24])
    return (width, height, header[25]) == (220, 132, 6)


def make_zip(source_root, entries, variant, archive_path, root):
    records = []
    for entry in sorted(entries, key=lambda item: item["filename"].casefold()):
        record = entry[variant]
        source = os.path.join(source_root, record["path"])
        with open(source, "rb") as stream:
            data = stream.read()
        if sha256_bytes(data) != record["sha256"]:
            raise ValueError("source PNG SHA256 mismatch: " + record["path"])
        if not png_is_220x132_rgba(source):
            raise ValueError("source PNG is not 220x132 RGBA: " + record["path"])
        records.append((root + "/" + entry["filename"], data))
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_STORED) as archive:
        folder = zipfile.ZipInfo(root + "/", (1980, 1, 1, 0, 0, 0))
        folder.create_system = 3
        folder.external_attr = (stat.S_IFDIR | 0o755) << 16
        archive.writestr(folder, b"")
        for member, data in records:
            info = zipfile.ZipInfo(member, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    source_root = os.path.realpath(args.source_root)
    output_dir = os.path.realpath(args.output_dir)
    git_head = os.popen("git -C %s rev-parse HEAD" % __import__("shlex").quote(source_root)).read().strip()
    if git_head != SOURCE_COMMIT:
        raise SystemExit("source checkout is not pinned to the approved PiconHub commit")
    catalog = load_verified_catalog(source_root)
    os.makedirs(output_dir, exist_ok=True)
    result = []
    for kind, variant, filename, root, expected_count in ARCHIVES:
        entries = [entry for entry in catalog["entries"] if entry["kind"] == kind]
        if len(entries) != expected_count:
            raise ValueError("unexpected archive count for %s/%s" % (kind, variant))
        path = os.path.join(output_dir, filename)
        make_zip(source_root, entries, variant, path, root)
        with open(path, "rb") as stream:
            payload = stream.read()
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                raise ValueError("generated ZIP CRC failure")
            names = [item.filename for item in archive.infolist() if not item.is_dir()]
            if len(names) != expected_count or any(not name.startswith(root + "/") for name in names):
                raise ValueError("generated ZIP member/root mismatch")
        result.append({"kind": kind, "variant": variant, "filename": filename,
                       "root": root, "png_count": expected_count,
                       "size": len(payload), "sha256": sha256_bytes(payload)})
    print(json.dumps({"source_repository": SOURCE_REPOSITORY, "source_commit": SOURCE_COMMIT,
                      "source_manifest_sha256": MANIFEST_SHA256,
                      "source_qc_checkpoint_provenance": EXPECTED_QC_PROVENANCE,
                      "archives": result},
                     sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
