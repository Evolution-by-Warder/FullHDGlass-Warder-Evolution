"""Regression tests for language-on-demand staging and atomic downloader."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
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

    def test_sync_updates_only_selected_language_and_works_offline_after_update(self):
        old = (PLUGIN / "locale/el/LC_MESSAGES/setupGlass17.mo").read_bytes()
        new = (PLUGIN / "locale/el/LC_MESSAGES/helpTxt.mo").read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = root / "locale"
            chosen = cache / "el/LC_MESSAGES/setupGlass17.mo"
            other = cache / "sk/LC_MESSAGES/setupGlass17.mo"
            for target in (chosen, other):
                target.parent.mkdir(parents=True)
                target.write_bytes(old)
            manifest = root / "manifest.json"
            digest = hashlib.sha256(new).hexdigest()
            manifest.write_text(json.dumps({"schema": 1, "ref": "a" * 40, "files": {
                "el": {"setupGlass17": digest}, "sk": {"setupGlass17": digest},
            }}))

            def open_catalog(request, *, timeout):
                self.assertIn("/locale/el/LC_MESSAGES/setupGlass17.mo", request.full_url)
                response = io.BytesIO(new)
                response.geturl = lambda: request.full_url
                return response

            with patch.object(downloader, "LOCALE", str(cache)), patch.object(
                downloader, "MANIFEST", str(manifest)
            ), patch.object(downloader, "urlopen", side_effect=open_catalog) as opener:
                self.assertEqual(downloader.sync("el_GR"), 1)
                self.assertEqual(downloader.sync("el_GR"), 0)
                self.assertEqual(downloader.sync("en_GB"), 0)
                self.assertEqual(opener.call_count, 1)
            self.assertEqual(chosen.read_bytes(), new)
            self.assertEqual(other.read_bytes(), old)

    def test_preinst_preserves_cached_languages_before_old_payload_is_removed(self):
        preinst = (ROOT / "source/control/preinst").read_text()
        migration = preinst.split("warder_preserve_locales() (", 1)[1].split(
            "\nif ! warder_preserve_locales", 1
        )[0]
        script = 'warder_preserve_locales() (' + migration + '\nwarder_preserve_locales "$@"'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin, cache, settings = (root / name for name in ("plugin", "state", "settings"))
            settings.write_text("config.osd.language=sq_AL\n")
            targets = [Path(lang) / "LC_MESSAGES/setupGlass17.mo" for lang in ("al", "sk")]
            catalogs = [(PLUGIN / "locale" / target).read_bytes() for target in targets]
            for target, catalog in zip(targets, catalogs):
                (plugin / "locale" / target).parent.mkdir(parents=True)
                (plugin / "locale" / target).write_bytes(catalog)
            args = ["sh", "-c", script, "preinst-test", str(plugin), str(cache), str(settings)]
            subprocess.run(args, check=True)
            self.assertEqual((cache / targets[0]).read_bytes(), catalogs[0])
            self.assertFalse((cache / targets[1]).exists())
            (plugin / "warder-locale-manifest.json").touch()
            (plugin / "locale" / targets[0]).write_bytes(b"older legacy catalog")
            subprocess.run(args, check=True)
            shutil.rmtree(plugin)
            for target, catalog in zip(targets, catalogs):
                self.assertEqual((cache / target).read_bytes(), catalog)

    def test_package_contains_only_english_and_digest_inventory(self):
        import gettext
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage = root / "stage"
            location = stage / builder.PLUGIN / "locale"
            shutil.copytree(PLUGIN / "locale", location)
            tarfile_path = root / "locale.tar.gz"
            builder.archive(stage, tarfile_path, payload=True)
            with tarfile.open(tarfile_path, "r:gz") as archive:
                names = archive.getnames()
                english = [n for n in names if n.endswith(".mo")]
                self.assertTrue(english)
                for name in english:
                    self.assertIn("/locale/en/LC_MESSAGES/", name)
                    catalog = gettext.GNUTranslations(archive.extractfile(name))
                    self.assertTrue(catalog.info()["language"].startswith("en"))
                self.assertFalse(any(n.endswith(".po") for n in names))
                record = next(n for n in names if n.endswith("warder-locale-manifest.json"))
                manifest = json.load(archive.extractfile(record))
            self.assertRegex(manifest["ref"], r"^[0-9a-f]{40}$")
            self.assertEqual(manifest["files"].keys(), downloader.LANGUAGES)
            for lang, signatures in manifest["files"].items():
                self.assertEqual(signatures.keys(), downloader.DOMAINS)
                for domain, digest in signatures.items():
                    source = location / lang / "LC_MESSAGES" / (domain + ".mo")
                    self.assertEqual(digest, hashlib.sha256(source.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
