#!/usr/bin/env python3
"""Deterministic FullHDGlass channel-picon package planner.

This tool intentionally does NOT download, resize, rerender or publish picons.
It consumes the audited SATLIST/Warder mapping and collision reports and emits a
stable build plan. Only source families proven by the audit are eligible.

The future materialization step must verify same-name blobs by content SHA and
must stop on every different-SHA collision recorded by the audit.
"""

from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAPPING = ROOT / "assets/warder/picon-satlist-mapping.tsv"
DEFAULT_COVERAGE = ROOT / "assets/warder/picon-warder-master-coverage.tsv"
DEFAULT_COLLISIONS = ROOT / "assets/warder/picon-collision-audit.tsv"

FAMILY_VARIANT = {
    "channel-transparent": "transparent",
    "channel-black": "black",
    "channel-white": "white",
}
UNRESOLVED_FAMILIES = (
    "channel-400x240",
    "channel-220x132",
    "channel-black-50x30",
    "channel-white-50x30",
    "channel-oled",
)


def read_tsv(path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    ap.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    ap.add_argument("--collisions", type=Path, default=DEFAULT_COLLISIONS)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    mapping = {r["selector_id"]: r for r in read_tsv(args.mapping)}
    coverage = {r["selector_id"]: r for r in read_tsv(args.coverage)}
    collision_rows = read_tsv(args.collisions)
    conflicts = {}
    for r in collision_rows:
        if r["selector_id"] in ("ALL_OTHER_MATCHED", "TOTAL"):
            continue
        conflicts.setdefault(r["selector_id"], {})[r["variant"]] = int(r["conflicting_names"])

    selectors = []
    for sid in sorted(mapping):
        m = mapping[sid]
        if m["warder_master_state"] != "MATCHED":
            selectors.append({
                "selector_id": sid,
                "warder_key": m["warder_key"],
                "state": "MISSING_SOURCE",
                "eligible_families": [],
                "blocked_families": list(FAMILY_VARIANT) + list(UNRESOLVED_FAMILIES),
            })
            continue

        c = coverage.get(sid)
        if not c:
            raise SystemExit("coverage missing for MATCHED selector: %s" % sid)

        eligible, blocked = [], list(UNRESOLVED_FAMILIES)
        for family, variant in FAMILY_VARIANT.items():
            if int(c[variant]) <= 0:
                blocked.append(family)
            elif conflicts.get(sid, {}).get(variant, 0):
                blocked.append(family)
            else:
                eligible.append(family)

        selectors.append({
            "selector_id": sid,
            "warder_key": m["warder_key"],
            "state": "READY" if eligible else "BLOCKED",
            "eligible_families": eligible,
            "blocked_families": sorted(blocked),
            "service_identities": int(c["service_identities"]),
        })

    doc = {
        "schema": 1,
        "authority": "PiconHub-Warder-Evolution/warder-master-production",
        "policy": {
            "deterministic": True,
            "silent_conflict_resolution": False,
            "resize_or_rerender": False,
            "runtime_switch": False,
        },
        "selectors": selectors,
    }
    payload = json.dumps(doc, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
