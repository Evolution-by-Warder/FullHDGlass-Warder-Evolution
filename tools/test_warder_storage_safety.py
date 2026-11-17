"""Regression checks for FullHDGlass receiver flash and external storage safety."""
import ast
import importlib.util
import pathlib
import tempfile
import types
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_DIR = ROOT / "source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
PLUGIN = MODULE_DIR / "plugin.py"
STORAGE = MODULE_DIR / "warderStorageSafety.py"
TEXTS = MODULE_DIR / "warderUiText.py"

spec = importlib.util.spec_from_file_location("warder_storage_under_test", STORAGE)
safe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(safe)


class StorageSafetyTests(unittest.TestCase):
    def check_mount(self, path, lines):
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as handle:
            handle.write(lines)
            handle.flush()
            # The mountinfo is synthetic; keep its target path stable.
            with mock.patch.object(safe.os.path, "realpath", side_effect=lambda value: value):
                return safe.is_internal(path, handle.name)

    def test_flash_root_and_unmounted_usb_are_internal(self):
        root = "22 1 0:1 / / rw - overlay overlay rw\n"
        self.assertTrue(self.check_mount("/etc/enigma2", root))
        self.assertTrue(self.check_mount("/media/usb/hdg17_files", root))
        self.assertTrue(self.check_mount("/media/hdd/hdg17_files", root))

    def test_mounted_hdd_usb_are_external(self):
        root = "22 1 0:1 / / rw - overlay overlay rw\n"
        usb = "23 22 8:1 / /media/usb rw - ext4 /dev/sda1 rw\n"
        hdd = "24 22 8:2 / /media/hdd rw - ext4 /dev/sdb2 rw\n"
        self.assertFalse(self.check_mount("/media/usb/hdg17_files", root + usb))
        self.assertFalse(self.check_mount("/media/hdd/hdg17_files", root + hdd))

    def test_internal_mmc_and_tmpfs_never_marked_external(self):
        root = "22 1 0:1 / / rw - overlay overlay rw\n"
        internal = "23 22 179:1 / /media/hdd rw - ext4 /dev/mmcblk0p2 rw\n"
        volatile = "24 22 0:3 / /media/usb rw - tmpfs tmpfs rw\n"
        self.assertTrue(self.check_mount("/media/hdd/hdg17_files", root + internal))
        self.assertTrue(self.check_mount("/media/usb/hdg17_files", root + volatile))

    def test_network_share_counts_as_external(self):
        root = "22 1 0:1 / / rw - overlay overlay rw\n"
        share = "23 22 0:45 / /media/nas rw - cifs //nas/hd rw\n"
        self.assertFalse(self.check_mount("/media/nas/hdg17_files", root + share))

    def test_unsafe_and_symlinked_paths_fail_closed(self):
        root = "22 1 0:1 / / rw - overlay overlay rw\n"
        self.assertTrue(self.check_mount("relative/path", root))
        self.assertTrue(self.check_mount("/tmp/hdg17_files", root))
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as handle:
            handle.write(root)
            handle.flush()
            with mock.patch.object(safe.os.path, "realpath", return_value="/etc"):
                self.assertTrue(safe.is_internal("/media/usb/alias", handle.name))

    def test_available_space_excludes_reserved_filesystem_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            free = types.SimpleNamespace(f_bfree=10000, f_bavail=500, f_frsize=4096)
            with mock.patch.object(safe.os, "statvfs", return_value=free):
                self.assertEqual(safe.available_bytes(directory), 500 * 4096)

    def test_reserve_enforced_even_after_user_confirms(self):
        reserve = safe.MIN_FREE_RESERVE
        with mock.patch.object(safe, "available_bytes", return_value=reserve + 1024):
            self.assertTrue(safe.has_space("/safe", additional_bytes=1024))
            self.assertFalse(safe.has_space("/safe", additional_bytes=1025))
            self.assertFalse(safe.has_space("/safe", additional_bytes=-1))
        with mock.patch.object(safe, "available_bytes", return_value=0):
            self.assertFalse(safe.has_space("/unknown"))

    def test_runtime_warns_and_keeps_selection_optional(self):
        text = PLUGIN.read_text(encoding="utf-8")
        ast.parse(text)
        self.assertIn('ui_text("Internal storage download warning")', text)
        self.assertIn('self.session.openWithCallback(self._warderStorageChoice, ChoiceBox', text)
        self.assertIn('ui_text("Continue anyway"), "continue"', text)
        self.assertIn('self._warderStorageSelected, dirBrowser', text)
        self.assertIn('if not _warderStorageHasSpace(target):', text)
        self.assertIn('setPathFiles(chck=False)', text)
        self.assertIn('config.plugins.setupGlass17.par124.save()', text)

    def test_unmounted_hdd_is_not_created_as_staging(self):
        text = PLUGIN.read_text(encoding="utf-8")
        section = text.split("def setWdir(self):", 1)[1].split("def doSelection", 1)[0]
        self.assertLess(section.index('_warderStorageIsInternal(os.path.dirname(HDDTMP))'),
                        section.index('os.makedirs(HDDTMP, exist_ok=True)'))
        self.assertIn('return "/tmp/"', section)

    def test_archive_preflight_precedes_removal_of_existing_icons(self):
        text = PLUGIN.read_text(encoding="utf-8")
        section = text.split('stage(_("Extracting")', 1)[1].split('self._safeExtractZip(target, base)', 1)[0]
        self.assertLess(section.index("unpacked_bytes = sum(info.file_size"),
                        section.index('self.rmTmp2(base, root)'))
        self.assertIn('not _warderStorageHasSpace(base, unpacked_bytes)', section)
        self.assertIn('not _warderStorageHasSpace(base, len(chunk))', text)
        self.assertIn('not _warderStorageHasSpace("/tmp", len(chunk))', text)

    def test_copy_to_internal_flash_is_atomic_and_checks_reserve(self):
        text = PLUGIN.read_text(encoding="utf-8")
        safe_copy = text.split("def _warderCopyWithStorageReserve(self, source, destination):", 1)[1].split("def cprmFiles(", 1)[0]
        self.assertIn("_warderStorageHasSpace(parent, os.path.getsize(source))", safe_copy)
        self.assertLess(safe_copy.index("tempfile.mkstemp"), safe_copy.index("os.replace(tmp, destination)"))
        self.assertIn("finally:", safe_copy)
        self.assertIn("os.unlink(tmp)", safe_copy)
        self.assertIn("shutil.copy2(source, destination)", safe_copy)
        copies = text.split("def cprmFiles(self, what):", 1)[1].split("def _warderFilesMatch(", 1)[0]
        self.assertEqual(copies.count("self._warderCopyWithStorageReserve(source, destination)"), 2)

    def test_storage_warning_translated_into_all_21_skin_languages(self):
        text = TEXTS.read_text(encoding="utf-8")
        tree = ast.parse(text)
        found = next(node for node in tree.body if isinstance(node, ast.Assign)
                     and any(isinstance(target, ast.Name) and target.id == "_STORAGE_WARNING_LABELS"
                             for target in node.targets))
        languages = ast.literal_eval(found.value)
        self.assertEqual(len(languages), 21)
        self.assertTrue(all(len(items) == 6 for items in languages.values()))


if __name__ == "__main__":
    unittest.main()
