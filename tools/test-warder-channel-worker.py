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


    def test_large_channel_zip_uses_selected_picon_disk_not_full_tmp(self):
        from unittest.mock import patch
        import os
        import types
        with tempfile.TemporaryDirectory() as root:
            received = []
            def fetch(job, archive, progress):
                self.assertEqual(Path(archive).parent, Path(root))
                self.assertTrue(Path(archive).name.startswith(".warder-channel-"))
                received.append(archive)
                Path(archive).write_bytes(b"verified-zip-stub")
                progress(12, 12)
            def install(archive, destination, wanted):
                self.assertEqual(Path(archive).read_bytes(), b"verified-zip-stub")
                self.assertEqual(destination, root)
                return {"test.png"}, {"test.png"}
            real_usage = worker_module.shutil.disk_usage
            def disk_usage(path):
                if os.path.realpath(path) == os.path.realpath("/tmp"):
                    raise AssertionError("/tmp must not be probed for channel archive space")
                self.assertEqual(path, root)
                return types.SimpleNamespace(free=1024 * 1024 * 1024)
            with patch.object(worker_module.shutil, "disk_usage", side_effect=disk_usage):
                worker = worker_module.ChannelWorker(
                    {"bytes": 12}, root, {"test.png"}, fetch, install)
                worker.run()
            self.assertEqual(list(worker.drain())[-1],
                             ("done", ({"test.png"}, {"test.png"})))
            self.assertEqual(len(received), 1)
            self.assertFalse(Path(received[0]).exists())
            self.assertEqual(list(Path(root).iterdir()), [])

    def test_insufficient_destination_space_fails_before_download(self):
        from unittest.mock import patch
        import types
        with tempfile.TemporaryDirectory() as root:
            called = []
            def should_not_fetch(*args):
                called.append("fetch")
            with patch.object(worker_module.shutil, "disk_usage",
                              return_value=types.SimpleNamespace(free=1024)):
                worker = worker_module.ChannelWorker(
                    {"bytes": 120 * 1024 * 1024}, root, None,
                    should_not_fetch, lambda *a: called.append("install"))
                worker.run()
            self.assertEqual(list(worker.drain())[-1],
                             ("error", "insufficient destination space for Warder channel package"))
            self.assertEqual(called, [])
            self.assertEqual(list(Path(root).iterdir()), [])

    def test_receiver_free_space_reserve_is_not_consumed_by_archive(self):
        from unittest.mock import patch
        import types
        with tempfile.TemporaryDirectory() as root:
            # 12-byte ZIP requires 10 MiB conservative overhead + 64 MiB
            # receiver reserve; 73 MiB is not enough to stage it safely.
            free = 73 * 1024 * 1024
            with patch.object(worker_module.shutil, "disk_usage",
                              return_value=types.SimpleNamespace(free=free)):
                worker = worker_module.ChannelWorker(
                    {"bytes": 12}, root, None,
                    lambda *a: self.fail("must not download into receiver reserve"),
                    lambda *a: self.fail("must not install"))
                worker.run()
            self.assertEqual(list(worker.drain())[-1],
                             ("error", "insufficient destination space for Warder channel package"))
            self.assertEqual(list(Path(root).iterdir()), [])

    def test_bad_archive_cleans_partial_zip_on_selected_storage(self):
        with tempfile.TemporaryDirectory() as root:
            staged = []
            def broken(job, archive, progress):
                staged.append(archive)
                Path(archive).write_bytes(b"partial")
                raise ValueError("SHA-256 mismatch")
            worker = worker_module.ChannelWorker(
                {"bytes": 12}, root, None, broken,
                lambda *args: self.fail("unverified package must not be installed"))
            worker.run()
            self.assertEqual(list(worker.drain())[-1],
                             ("error", "SHA-256 mismatch"))
            self.assertTrue(staged)
            self.assertFalse(Path(staged[0]).exists())

    def test_symlink_destination_is_not_used_as_temporary_archive(self):
        import os
        with tempfile.TemporaryDirectory() as root:
            actual = Path(root) / "real"
            actual.mkdir()
            link = Path(root) / "link"
            link.symlink_to(actual, target_is_directory=True)
            worker = worker_module.ChannelWorker(
                {"bytes": 12}, str(link), None,
                lambda *a: self.fail("unsafe destination must not download"),
                lambda *a: self.fail("unsafe destination must not install"))
            worker.run()
            self.assertEqual(list(worker.drain())[-1],
                             ("error", "unsafe Warder picon destination"))
            self.assertEqual(list(actual.iterdir()), [])


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
            self.assertIn(("stage", "download"), events)
            self.assertIn(("stage", "extract"), events)

    def test_legacy_copy_worker_isolated_result(self):
        visited = []
        def copy(folder):
            visited.append(folder)
            return 9, 10
        worker = worker_module.LegacyCopyWorker(copy, "picon_50x30")
        worker.start()
        worker.thread.join(timeout=5)
        self.assertFalse(worker.thread.is_alive())
        self.assertEqual(visited, ["picon_50x30"])
        self.assertEqual(list(worker.drain()), [("done", (9, 10))])

    def test_legacy_copy_worker_reports_failure(self):
        def broken(folder):
            raise OSError("storage disconnected")
        worker = worker_module.LegacyCopyWorker(broken, "picon")
        worker.start()
        worker.thread.join(timeout=5)
        self.assertEqual(list(worker.drain()), [("error", "storage disconnected")])

    def test_canonical_worker_reports_stages_and_verified_result(self):
        def install(row, variant, progress, stage):
            self.assertEqual((row, variant), ("aux-prov", "black"))
            stage("catalog")
            stage("download")
            progress(3, 4)
            stage("extract")
            stage("copy")
            return "SUCCESSFUL: 2/2"
        worker = worker_module.CanonicalWorker("aux-prov", "black", install)
        worker.start()
        worker.thread.join(timeout=5)
        self.assertFalse(worker.thread.is_alive())
        self.assertEqual(list(worker.drain()), [
            ("stage", "catalog"), ("stage", "download"),
            ("bytes", (3, 4)), ("stage", "extract"),
            ("stage", "copy"), ("done", "SUCCESSFUL: 2/2")])

    def test_canonical_worker_propagates_verification_failure(self):
        def broken(row, variant, progress, stage):
            stage("download")
            raise ValueError("SHA-256 mismatch")
        worker = worker_module.CanonicalWorker("aux-sat", "white", broken)
        worker.start()
        worker.thread.join(timeout=5)
        self.assertEqual(list(worker.drain()), [
            ("stage", "download"), ("error", "SHA-256 mismatch")])


if __name__ == "__main__":
    unittest.main()
