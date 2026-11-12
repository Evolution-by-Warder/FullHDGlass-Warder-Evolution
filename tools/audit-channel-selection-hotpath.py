#!/usr/bin/env python3
"""Source-level ChannelSelection hot-path audit; NOT a receiver speed benchmark.

Analyze the *shipped* renderer Python AST to identify repeated work on the
Enigma2 GUI thread. Keep expensive performance conclusions conditional until
receiver instrumentation supplies timings.
"""
import argparse
import ast
import json
from pathlib import Path

DEFAULT = Path("source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderChannelEpgClip.py")


def method(cls, name):
    return next(n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)


def calls(node, name):
    return [x for x in ast.walk(node) if isinstance(x, ast.Call)
            and isinstance(x.func, ast.Attribute) and x.func.attr == name]


def audit(path, visible_rows=14):
    src = Path(path).read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(path))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "WarderChannelEpgClip")
    refresh = method(cls, "refresh")
    draw = method(cls, "_draw_rows")
    name_event = method(cls, "_name_and_event")
    progress = method(cls, "_progress_fraction")
    starts = [c for c in calls(refresh, "start") if c.args and isinstance(c.args[0], ast.Constant)
              and isinstance(c.args[0].value, int)]
    intervals = sorted(set(c.args[0].value for c in starts))
    if not intervals or min(intervals) <= 0:
        raise ValueError("Cannot determine active refresh timer interval")
    interval_ms = min(intervals)
    per_row_name = len(calls(draw, "_name_and_event"))
    per_row_progress = len(calls(draw, "_progress_fraction"))
    native_name_event = len(calls(name_event, "getEvent"))
    native_progress_event = len(calls(progress, "getEvent"))
    # These are SOURCE-LEVEL UPPER-BOUND WORKLOAD ESTIMATES, not measured counts:
    # loop branches, empty EPG entries, unsupported modes and list visibility
    # can reduce actual calls; other renderers may add work independently.
    event_queries_per_visible_row = (per_row_name * native_name_event
                                     + per_row_progress * native_progress_event)
    hz = 1000.0 / interval_ms
    result = {
        "kind": "static-hot-path-audit-not-receiver-benchmark",
        "source": str(path),
        "refresh_interval_ms": interval_ms,
        "scheduled_refreshes_per_second": round(hz, 2),
        "estimated_visible_rows": visible_rows,
        "potential_native_getEvent_calls_per_visible_row_per_refresh": event_queries_per_visible_row,
        "potential_native_getEvent_calls_per_refresh": visible_rows * event_queries_per_visible_row,
        "potential_native_getEvent_calls_per_second": round(hz * visible_rows * event_queries_per_visible_row),
        "text_measurement_call_sites_in_row_draw": len(calls(draw, "calculateSize")),
        "native_service_info_per_refresh": per_row_name,
        "native_progress_computations_per_refresh": per_row_progress,
        "requires_receiver_timing_to_confirm_cause": True,
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT)
    parser.add_argument("--visible-rows", type=int, default=14)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 1 <= args.visible_rows <= 100:
        parser.error("--visible-rows must be 1..100")
    result = audit(args.source, args.visible_rows)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
