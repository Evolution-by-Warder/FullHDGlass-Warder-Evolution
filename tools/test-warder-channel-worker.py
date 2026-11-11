#!/usr/bin/env python3
"""Offline tests for GUI-safe background Warder channel downloads."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderChannelWorker.py"
spec = importlib.util.spec_from_file_location("warderChannelWorker", MODULE)
worker_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker_module)


class ChannelWorkerTests(unittest.TestCase):
    def test_manifest_done_and_error_events(self):
        success = worker_module.ManifestWorker("manifest", lambda url: {"url": url})
        success.start()
        success.thread.join(timeout=5)
        self.assertFalse(success.thread.is_alive())
        self.assertEqual(list(success.drain()), [("done", {"url": "manifest"})])

        def broken(url):
            raise ValueError("invalid manifest")
        failure = worker_module.ManifestWorker("manifest", broken)
        failure.start()
        failure.thread.join(timeout=5)
        self.assertEqual(list(failure.drain()), [("error", "invalid manifest")])

    def test_package_reports_bytes_stages_and_result(self):
        with tempfile.TemporaryDirectory() as root:
            def fetch(job, archive, progress):
                Path(archive).write_bytes(b"test")
                progress(2, 4)
                progress(4, 4)

            def install(archive, destination, wanted):
                self.assertEqual(Path(archive).read_bytes(), b"test")
                self.assertEqual(wanted, {"a.png"})
                return {"a.png"}, {"a.png", "b.png"}

            worker = worker_module.ChannelWorker(
                {"bytes": 4}, root, {"a.png"}, fetch, install)
            worker.start()
            worker.thread.join(timeout=5)
            self.assertFalse(worker.thread.is_alive())
            events = list(worker.drain())
            self.assertIn(("bytes", (2, 4)), events)
            self.assertIn(("bytes", (4, 4)), events)
            self.assertEqual(events[-1], ("done", ({"a.png"}, {"a.png", "b.png"})))

    def test_package_failure_does_not_report_success(self):
        with tempfile.TemporaryDirectory() as root:
            def broken(job, archive, progress):
                raise ValueError("SHA-256 mismatch")

            worker = worker_module.ChannelWorker(
                {"bytes": 4}, root, None, broken,
                lambda *args: self.fail("install must not be called"))
            worker.start()
            worker.thread.join(timeout=5)
            self.assertEqual(list(worker.drain())[-1],
                             ("error", "SHA-256 mismatch"))

    def test_auxiliary_asset_worker_reports_progress(self):
        with tempfile.TemporaryDirectory() as root:
            def work(asset, target, progress, stage):
                stage('Checking archive')
                progress(1, 2)
                progress(2, 2)
                self.assertEqual(asset["root"], "icons")
                self.assertTrue(target.endswith("asset.zip"))
                return "icons"
            worker = worker_module.AssetWorker(
                {"root": "icons"}, str(Path(root) / "asset.zip"), work)
            worker.start()
            worker.thread.join(timeout=5)
            self.assertFalse(worker.thread.is_alive())
            self.assertEqual(list(worker.drain()), [
                ("stage", "Checking archive"), ("bytes", (1, 2)),
                ("bytes", (2, 2)), ("done", "icons")])

    def test_auxiliary_asset_worker_propagates_error(self):
        def reject(asset, target, progress, stage):
            raise ValueError("unsafe asset redirect")
        worker = worker_module.AssetWorker(
            {"root": "icons"}, "/tmp/asset.zip", reject)
        worker.start()
        worker.thread.join(timeout=5)
        self.assertFalse(worker.thread.is_alive())
        self.assertEqual(list(worker.drain()), [
            ("error", "unsafe asset redirect")])

    def test_legacy_worker_rejects_untrusted_download(self):
        with tempfile.TemporaryDirectory(dir="/tmp") as root:
            worker = worker_module.LegacyArchiveWorker(
                "https://example.invalid/archive.7z", str(Path(root) / "unpack"),
                str(Path(root) / "7z"))
            worker.start()
            worker.thread.join(timeout=5)
            self.assertFalse(worker.thread.is_alive())
            self.assertIn("untrusted preserved legacy archive",
                          str(list(worker.drain())[-1]))

    def test_legacy_worker_streams_and_extracts_approved_archive(self):
        from unittest.mock import patch
        import io

        class Response(io.BytesIO):
            def __init__(self, url):
                super().__init__(b"TEST")
                self.url = url
                self.headers = {"Content-Length": "4"}
            def geturl(self):
                return self.url

        class Opener:
            def open(self, request, timeout=15):
                return Response(request.full_url)

        with tempfile.TemporaryDirectory(dir="/tmp") as root:
            executable = Path(root) / "7z"
            executable.write_text("fake 7zip fixture")
            target = str(Path(root) / "unpack")
            url = worker_module.LegacyArchiveWorker._ROOT + "verified.7z"
            with patch("urllib.request.build_opener", return_value=Opener()), patch("subprocess.call", return_value=0):
                worker = worker_module.LegacyArchiveWorker(url, target, str(executable))
                worker.start()
                worker.thread.join(timeout=5)
            self.assertFalse(worker.thread.is_alive())
            events = list(worker.drain())
            self.assertIn(("bytes", (4, 4)), events)
            self.assertEqual(events[-1], ("done", 4))
            self.assertTrue(any(x[0] == "stage" and "Extracting" in x[1]
                                for x in events))


if __name__ == "__main__":
    unittest.main()
