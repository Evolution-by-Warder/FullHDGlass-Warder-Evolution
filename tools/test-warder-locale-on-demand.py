"""Regression tests for language-on-demand staging and atomic downloader."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


downloader = load(PLUGIN / "warderLocaleDownload.py", "locale_download_test")
builder = load(ROOT / "tools/build-release-ipk.py", "locale_package_test")


class TestOnDemand(unittest.TestCase):
    def test_language_aliases_and_english_no_download(self):
        self.assertEqual(downloader.normalize("sq_AL"), "al")
        self.assertEqual(downloader.normalize("el_GR"), "el")
        self.assertEqual(downloader.normalize("sk_SK"), "sk")
        self.assertEqual(downloader.sync("en_GB"), 0)

    def test_verified_cached_catalogue_needs_no_network(self):
        original = (PLUGIN / "locale/el/LC_MESSAGES/setupGlass17.mo").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "locale/el/LC_MESSAGES"
            folder.mkdir(parents=True)
            (folder / "setupGlass17.mo").write_bytes(original)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"schema": 1, "ref": "a" * 40,
                         "files": {"el": {"setupGlass17": hashlib.sha256(original).hexdigest()}}}))
            with patch.object(downloader, "LOCALE", str(root / "locale")), patch.object(
                downloader, "MANIFEST", str(manifest)), patch.object(downloader, "urlopen") as opener:
                self.assertEqual(downloader.sync("el_GR"), 0)
                opener.assert_not_called()

    def test_bad_download_preserves_existing_catalogue(self):
        from unittest.mock import MagicMock
        original = (PLUGIN / "locale/el/LC_MESSAGES/setupGlass17.mo").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "locale/el/LC_MESSAGES"
            folder.mkdir(parents=True)
            target = folder / "setupGlass17.mo"
            target.write_bytes(original)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"schema": 1, "ref": "a" * 40,
                         "files": {"el": {"setupGlass17": "0" * 64}}}))
            response = MagicMock()
            response.__enter__.return_value = response
            response.geturl.return_value = downloader.BASE + "a" * 40 + (
                "/source/package-root/usr/lib/enigma2/python/Plugins/Extensions/"
                "setupGlass17/locale/el/LC_MESSAGES/setupGlass17.mo")
            response.read.return_value = b"corrupted file"
            with patch.object(downloader, "LOCALE", str(root / "locale")), patch.object(
                downloader, "MANIFEST", str(manifest)), patch.object(
                downloader, "urlopen", return_value=response):
                with self.assertRaises(ValueError):
                    downloader.sync("el")
            self.assertEqual(target.read_bytes(), original)

    def test_package_contains_only_english_and_digest_inventory(self):
        original = (PLUGIN / "locale/el/LC_MESSAGES/setupGlass17.mo").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            location = root / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/locale"
            for lang in ("el", "en"):
                folder = location / lang / "LC_MESSAGES"
                folder.mkdir(parents=True)
                (folder / "setupGlass17.mo").write_bytes(original)
            (location / "el/LC_MESSAGES/setupGlass17.po").write_text("source")
            tarfile_path = root.parent / (root.name + "-locale.tar.gz")
            try:
                builder.archive(root, tarfile_path, payload=True)
                with tarfile.open(tarfile_path, "r:gz") as archive:
                    names = archive.getnames()
                    self.assertTrue(any("/en/LC_MESSAGES/setupGlass17.mo" in n for n in names))
                    self.assertFalse(any("/el/LC_MESSAGES/setupGlass17.mo" in n for n in names))
                    self.assertFalse(any(n.endswith(".po") for n in names))
                    record = next(n for n in names if n.endswith("warder-locale-manifest.json"))
                    manifest = json.load(archive.extractfile(record))
                    self.assertEqual(manifest["files"]["el"]["setupGlass17"], hashlib.sha256(original).hexdigest())
                    self.assertEqual(len(manifest["ref"]), 40)
            finally:
                tarfile_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
