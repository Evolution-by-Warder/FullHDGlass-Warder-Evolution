#!/usr/bin/env python3
"""Regression test for clean removal without touching external user data."""
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTRM = (ROOT / "source/control/postrm").read_text()

def run(scenario):
    with tempfile.TemporaryDirectory(prefix="warder-remove-") as folder:
        root = Path(folder)
        skin = root / "usr/share/enigma2/hd_glass17"
        plugin = root / "usr/lib/enigma2/python/Plugins/Extensions/setupGlass17"
        state = root / "var/lib/fullhdglass17"
        external = root / "media/external"
        external.mkdir(parents=True)
        (external / "valuable-picons.txt").write_text("keep")
        for path in (skin, plugin, state):
            path.mkdir(parents=True)
            (path / "untracked-file").write_text("obsolete")
        settings = root / "etc/enigma2/settings"
        settings.parent.mkdir(parents=True)
        settings.write_text("config.plugins.setupGlass17.par125=" + str(root / "media/usb") + "\nkeep-enigma2-config")
        own_data = root / "media/usb/hdg17_files"
        own_data.mkdir(parents=True)
        (own_data / "picon").mkdir()
        (own_data / "picon" / "warder-owned.png").write_bytes(b"ours")
        old_data = root / "media/other-storage/hdg17_files"
        old_data.mkdir(parents=True)
        (old_data / "old-warder.png").write_bytes(b"ours")
        (state / "data-paths-v1.list").write_text(
            str(own_data) + "\n" + str(old_data) + "\n")
        other_data = root / "media/other-storage/unrelated"
        other_data.mkdir()
        (other_data / "keep.png").write_bytes(b"theirs")
        other_picons = root / "media/usb/picon"
        other_picons.mkdir(parents=True)
        (other_picons / "keep.png").write_bytes(b"theirs")
        shell = POSTRM
        for original in (
            "/usr/share/enigma2/hd_glass17",
            "/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17",
            "/var/lib/fullhdglass17",
            "/etc/enigma2/skin_user-ori17.xml",
            "/etc/enigma2/skin_user.xml",
            "/usr/share/enigma2/encoding-ori17.conf",
            "/usr/share/enigma2/encoding.conf",
            "/usr/lib/enigma2/python/Screens",
            "/media/usb",
            "/etc/enigma2/settings",
        ):
            shell = shell.replace(original, str(root / original.lstrip("/")))
        script = root / "postrm"
        script.write_text(shell)
        assert subprocess.run(["sh", "-n", str(script)], check=False).returncode == 0
        if scenario == "upgrade":
            command = "upgrade"
        elif scenario == "symlink":
            # An untracked symlink inside the skin is NOT a reason to delete
            # the target: GNU rm -rf only unlinks the symlink itself.
            (skin / "external-link").symlink_to(external, target_is_directory=True)
            command = "remove"
        else:
            command = "remove"
        result = subprocess.run(["sh", str(script), command], capture_output=True, text=True)
        assert result.returncode == 0, (scenario, result.stdout, result.stderr)
        for path in (skin, plugin, state):
            assert path.exists() == (scenario == "upgrade"), (scenario, path)
        assert settings.read_text() == "config.plugins.setupGlass17.par125=" + str(root / "media/usb") + "\\nkeep-enigma2-config"
        assert own_data.exists() == (scenario == "upgrade"), (scenario, own_data)
        assert old_data.exists() == (scenario == "upgrade"), (scenario, old_data)
        assert (other_data / "keep.png").read_bytes() == b"theirs"
        assert (other_picons / "keep.png").read_bytes() == b"theirs"
        assert (external / "valuable-picons.txt").read_text() == "keep"

if __name__ == "__main__":
    for scenario in ("upgrade", "remove", "symlink"):
        run(scenario)
    print("PASS: full directory removal, upgrade preservation and external data safety")
