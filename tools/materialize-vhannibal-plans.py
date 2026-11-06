#!/usr/bin/env python3
"""Write the PR #42 plans.json from the pinned PR #41 input and resolution evidence.

Run from a checkout with: python tools/materialize-vhannibal-plans.py /tmp/plans.json
The pinned input remains available for reproducing the earlier catalogue.
"""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import tarfile


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "reports/vhannibal-final-live-input"
REPORT = ROOT / "reports/vhannibal-six-resolutions-20261105"
VARIANTS = {
    f"{size}|channel-{background}"
    for size in ("50x30", "220x132", "400x240")
    for background in ("transparent", "white", "black")
}


def verified(data, digest, label, size=None):
    if sha256(data).hexdigest() != digest or (size is not None and len(data) != size):
        raise ValueError(f"Integrity check failed for {label}")
    return data


def read_pinned_plans():
    manifest = json.loads((INPUT / "input-manifest.json").read_bytes())
    payload = b"".join(
        verified((INPUT / part["filename"]).read_bytes(), part["sha256"],
                 part["filename"], part["bytes"])
        for part in manifest["parts"]
    )
    verified(payload, manifest["sha256"], "Vhannibal input archive", manifest["bytes"])
    with tarfile.open(fileobj=BytesIO(payload), mode="r:gz") as archive:
        plans = archive.extractfile("plans.json").read()
    return json.loads(verified(plans, manifest["members"]["plans.json"], "plans.json"))


def by_reference(rows):
    result = {row["reference"]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError("Duplicate full service reference in plans")
    return result


def reconcile():
    plans = by_reference(read_pinned_plans())
    resolved = by_reference(json.loads((REPORT / "resolved-plans.json").read_bytes()))
    cases = json.loads((REPORT / "resolutions.json").read_bytes())["cases"]
    assets = json.loads((REPORT / "asset-index.json").read_bytes())
    verification = json.loads((REPORT / "live-verification.json").read_bytes())
    accepted = by_reference([
        {**case, "reference": ref}
        for case in cases for ref in case.get("references", [])
    ])
    excluded = {case["reference"] for case in cases if case["status"].startswith("EXCLUDED_")}
    if accepted.keys() != resolved.keys() or excluded & (plans.keys() | resolved.keys()):
        raise ValueError("Resolution rows disagree with the accepted or excluded references")
    if len(resolved.keys() - plans.keys()) != verification["new_current_references"]:
        raise ValueError("New reference count differs from the candidate verification")
    if len(resolved.keys() & plans.keys()) != verification["existing_same_programme_reference_corrected"]:
        raise ValueError("Corrected reference count differs from the candidate verification")
    if len(plans.keys() | resolved.keys()) != verification["accepted_current_references"]:
        raise ValueError("Accepted reference total differs from the candidate verification")

    for ref, row in resolved.items():
        case = accepted[ref]
        asset_key = row["asset_key"]
        variants = assets[asset_key]
        if case["asset_key"] != asset_key or variants.keys() != VARIANTS:
            raise ValueError(f"Incorrect artwork binding or incomplete variants for {ref}")
        # Keep the superseded decision as provenance. The resolved choice and
        # hashes describe the candidate packages.
        previous = {
            field: row.pop(field)
            for field in ("choice", "hold_reason", "source", "asset_id")
            if field in row
        }
        if ref in plans:
            identity = {key: value for key, value in row.items() if key not in ("asset_key", "operation")}
            if {**identity, **previous} != plans[ref]:
                raise ValueError(f"Correction would overwrite the original source record for {ref}")
        plans[ref] = {
            **row,
            "choice": row["operation"],
            "resolution_status": case["status"],
            "variant_sha256": {variant: item["sha256"] for variant, item in variants.items()},
            "previous_decision": previous,
        }
    return list(plans.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Path for the reconciled plans.json")
    output = parser.parse_args().output
    plans = reconcile()
    with output.open("x", encoding="utf-8") as stream:
        json.dump(plans, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(f"Reconciled {len(plans)} accepted Vhannibal references")


if __name__ == "__main__":
    main()
