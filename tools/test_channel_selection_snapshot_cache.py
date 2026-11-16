"""TEST4 source-method regression: short-lived EPG snapshot cache.

Runs actual renderer methods with a deterministic fake service center/clock.
Does not pretend to measure the receiver GPU or keypress latency.
"""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderChannelEpgClip.py"
tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
klass = next(n for n in tree.body if isinstance(n, ast.ClassDef)
             and n.name == "WarderChannelEpgClip")
names = {"_event_snapshot", "_name_and_event", "_progress_fraction"}
nodes = [n for n in klass.body if isinstance(n, ast.FunctionDef) and n.name in names]
clock = [100.0]
env = {"monotonic": lambda: clock[0], "time": lambda: 180.0}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), "exec"), env)


class Event:
    def __init__(self, name="Show A", start=120, duration=120):
        self.name, self.start, self.duration = name, start, duration

    def getEventName(self):
        return self.name

    def getDuration(self):
        return self.duration

    def getBeginTime(self):
        return self.start


class Ref:
    flags = 0

    def __init__(self, ident):
        self.ident = ident

    def toString(self):
        return self.ident


class Center:
    def __init__(self):
        self.calls = 0
        self.events = {"first": Event(), "second": Event("Show B")}

    def info(self, ref):
        self.calls += 1
        return SimpleNamespace(
            getName=lambda value: "Channel " + value.ident,
            getEvent=lambda value: self.events.get(value.ident))


class Target:
    _event_snapshot = env["_event_snapshot"]
    _name_and_event = env["_name_and_event"]
    _progress_fraction = env["_progress_fraction"]

    def __init__(self):
        self._epg_snapshots = {}
        self._epg_cache_hits = 0
        self._epg_cache_misses = 0
        self._perf_name_calls = 0
        self._perf_progress_calls = 0


class EpgCacheTests(unittest.TestCase):
    def setUp(self):
        clock[0] = 100.0
        self.center = Center()
        self.target = Target()
        self.first = Ref("first")

    def test_title_and_progress_use_one_native_lookup(self):
        for _ in range(20):
            self.assertEqual(self.target._name_and_event(self.center, self.first),
                             ("Channel first", "Show A"))
            self.assertEqual(self.target._progress_fraction(self.center, self.first), 0.5)
        self.assertEqual(self.center.calls, 1)
        self.assertEqual(self.target._epg_cache_misses, 1)
        self.assertEqual(self.target._epg_cache_hits, 39)

    def test_cache_expires_after_one_second_and_updates_programme(self):
        self.target._name_and_event(self.center, self.first)
        clock[0] += .99
        self.center.events["first"] = Event("New programme")
        self.assertEqual(self.target._name_and_event(self.center, self.first)[1], "Show A")
        clock[0] += .02
        self.assertEqual(self.target._name_and_event(self.center, self.first)[1], "New programme")
        self.assertEqual(self.center.calls, 2)

    def test_different_service_never_inherits_stale_event(self):
        self.assertEqual(self.target._name_and_event(self.center, self.first)[1], "Show A")
        self.assertEqual(self.target._name_and_event(self.center, Ref("second"))[1], "Show B")
        self.assertEqual(self.center.calls, 2)

    def test_missing_epg_is_cached_briefly_and_can_recover(self):
        ref = Ref("missing")
        self.assertEqual(self.target._name_and_event(self.center, ref)[1], "")
        self.assertIsNone(self.target._progress_fraction(self.center, ref))
        self.assertEqual(self.center.calls, 1)
        self.center.events["missing"] = Event("Found")
        clock[0] += 1.01
        self.assertEqual(self.target._name_and_event(self.center, ref)[1], "Found")
        self.assertEqual(self.center.calls, 2)

    def test_marker_is_never_queried(self):
        ref = Ref("marker")
        ref.flags = 7
        self.assertEqual(self.target._name_and_event(self.center, ref), ("", ""))
        self.assertIsNone(self.target._progress_fraction(self.center, ref))
        self.assertEqual(self.center.calls, 0)

    def test_cache_is_bounded_during_long_browsing(self):
        for index in range(220):
            self.target._event_snapshot(self.center, Ref("service-%d" % index))
        self.assertLessEqual(len(self.target._epg_snapshots), 96)

    def test_event_progress_remains_time_based_even_with_cached_event(self):
        self.assertEqual(self.target._progress_fraction(self.center, self.first), 0.5)
        env["time"] = lambda: 210.0
        try:
            self.assertEqual(self.target._progress_fraction(self.center, self.first), 0.75)
            self.assertEqual(self.center.calls, 1)
        finally:
            env["time"] = lambda: 180.0


if __name__ == "__main__":
    unittest.main()
