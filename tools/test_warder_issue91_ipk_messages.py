"""Issue #91: test FullHDGlass IPK lifecycle messages without building an IPK.

Never execute uninstall cleanup in a test; it removes package-owned skin files.
"""
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "source/control"
BAR = "*" * 66
NAME = "FullHDGlass Warder Evolution"


def hook(name):
    return (CONTROL / name).read_text(encoding="utf-8")


class SkinLifecycleMessages(unittest.TestCase):
    def test_all_shell_hooks_have_expected_separator_and_syntax(self):
        for name in ("preinst", "postinst", "prerm", "postrm"):
            with self.subTest(name=name):
                script = hook(name)
                self.assertTrue(script.startswith("#!/bin/sh\n"))
                self.assertIn('echo "' + BAR + '"', script)
                subprocess.run(["sh", "-n"], input=script, text=True, check=True)

    def test_install_completion_never_precedes_health_check(self):
        script = hook("postinst")
        self.assertLess(script.index("warderInstallHealth.py --payload-only"),
                        script.index("Install/upgrade/reinstall finished: " + NAME))
        self.assertIn("Existing FullHDGlass settings were preserved.", script)
        self.assertIn("Please restart GUI to activate changes.", script)
        self.assertIn("Preparing FullHDGlass Warder Evolution upgrade/reinstall...", hook("preinst"))

    def test_actual_remove_and_upgrade_are_distinguished(self):
        # prerm upgrade does not run destructive cleanup.
        script = hook("prerm")
        result = subprocess.run(["sh", "-c", script, "warder-hook", "upgrade"],
                                capture_output=True, text=True, timeout=8, check=True)
        self.assertIn("upgrade/reinstall", result.stdout)
        self.assertNotIn("Removing", result.stdout)
        postrm = hook("postrm")
        self.assertLess(postrm.index('case "\${1:-}" in'), postrm.index("Removal finished: " + NAME))
        self.assertIn("remove|purge)", postrm)
        self.assertIn("*) exit 0 ;;", postrm)
        # Only 'upgrade' is executed: 'remove' would delete the real skin!
        result = subprocess.run(["sh", "-c", postrm, "warder-hook", "upgrade"],
                                capture_output=True, text=True, timeout=8, check=True)
        self.assertEqual(result.stdout, "")

    def test_existing_safety_controls_are_untouched(self):
        self.assertIn("warderPackageTransition.py backup", hook("prerm"))
        self.assertIn("warderPackageTransition.py restore", hook("postinst"))
        self.assertIn("warder_remove_install_dir", hook("postrm"))
        self.assertIn("Saved Enigma2 settings were left intact.", hook("postrm"))


if __name__ == "__main__":
    unittest.main()
