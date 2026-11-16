#!/usr/bin/env python3
"""Offline test of the optional RADIO artwork timing hook.

Extracts the actual renderer worker by AST; no Enigma2 GUI modules are loaded.
"""
import ast
import hashlib
import io
import os
import re
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "source/package-root/usr/lib/enigma2/python/Components/Renderer/WarderRadioArtwork.py"
MARKER = "/tmp/warder-radio-cover-benchmark"


class Collect(io.StringIO):
    def __init__(self, sink):
        super().__init__()
        self.sink = sink

    def __exit__(self, exc_type, exc, tb):
        self.sink.append(self.getvalue())
        self.close()


class InlineThread:
    def __init__(self, target):
        self.target = target
        self.daemon = False

    def start(self):
        self.target()


class ArtworkBenchmarkTests(unittest.TestCase):
    def test_no_write_without_explicit_marker_and_bounded_output_with_marker(self):
        tree = ast.parse(RENDERER.read_text(encoding="utf-8"))
        cls = next(c for c in tree.body if isinstance(c, ast.ClassDef)
                   and c.name == "WarderRadioArtwork")
        method = next(m for m in cls.body if isinstance(m, ast.FunctionDef)
                      and m.name == "_request")
        records, queries = [], []
        marker_present = [False]
        def isfile(path):
            return marker_present[0] and path == MARKER
        def write_log(path, mode):
            self.assertEqual(path, MARKER + ".log")
            self.assertEqual(mode, "a")
            return Collect(records)
        def lookup_cover(artist, title):
            queries.append((artist, title))
            return "/tmp/fake-artwork.jpg", "TheAudioDB"

        environment = {
            "hashlib": hashlib, "time": time,
            "os": SimpleNamespace(
                path=SimpleNamespace(join=os.path.join, isfile=isfile,
                                     getsize=lambda path: 0),
                replace=lambda *args: self.fail("unexpected rotation")),
            "open": write_log,
            "threading": SimpleNamespace(Thread=InlineThread),
            "cover_search": SimpleNamespace(lookup_cover=lookup_cover)
        }
        exec(compile(ast.fix_missing_locations(
                 ast.Module(body=[method], type_ignores=[])), str(RENDERER), "exec"),
             environment)
        request = environment["_request"]

        class Dummy:
            _generation = 12
            _result = None
            _busy = False
            _attempts = 0
            def _cacheDir(self):
                return "/tmp/warder-radio-artwork"
            def _diag(self, message):
                pass

        box = Dummy()
        request(box, "ABBA", "Dancing Queen", "abba|dancing queen")
        self.assertEqual(len(records), 0, "Benchmark should be disabled by default")
        self.assertEqual(box._result, (12, "abba|dancing queen", "/tmp/fake-artwork.jpg"))
        marker_present[0] = True
        request(box, "ABBA", "Mamma Mia", "abba|mamma mia")
        self.assertEqual(len(records), 1)
        self.assertRegex(records[0], r"^ms=\d+ result=hit source=TheAudioDB track=[0-9a-f]{12}\n$")
        self.assertEqual(len(queries), 2)


if __name__ == "__main__":
    unittest.main()
