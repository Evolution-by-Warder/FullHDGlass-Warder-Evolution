"""Preserve receiver-owned skin state across the package-name transition."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

FILES = (
    "/etc/enigma2/skin_user-hdg17.xml", "/etc/enigma2/skin_user.xml",
    "/usr/share/enigma2/encoding.conf",
    "/usr/lib/enigma2/python/Screens/ChannelSelection.py",
    "/usr/lib/enigma2/python/Screens/Menu.py",
    "/usr/lib/enigma2/python/Screens/Menu.pyc",
    "/usr/lib/enigma2/python/Screens/Menu.pyo",
    "/var/lib/fullhdglass17/epg-default-v1.state",
    "/etc/enigma2/skin_user-ori17.xml", "/usr/share/enigma2/encoding-ori17.conf",
    "/usr/lib/enigma2/python/Screens/ChannelSelection.py-ori17.py",
    "/usr/lib/enigma2/python/Screens/Menu.py-orig17.py",
    "/usr/lib/enigma2/python/Screens/Menu.py-orig17.pyc",
    "/usr/lib/enigma2/python/Screens/Menu.py-orig17.pyo",
)
STATE = "var/lib/fullhdglass17/package-transition-v1"


def local(root, path):
    return Path(root) / path.lstrip("/")


def backup(root="/"):
    folder = local(root, STATE)
    if folder.is_symlink():
        raise ValueError("Unsafe transition state")
    if folder.exists():
        verify(folder)
        return
    folder.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".package-transition-", dir=str(folder.parent)))
    try:
        entries = []
        for number, path in enumerate(FILES):
            source = local(root, path)
            if source.is_symlink():
                entries.append({"path": path, "link": os.readlink(str(source))})
            elif source.is_file():
                target = stage / str(number)
                shutil.copy2(str(source), str(target))
                entries.append({"path": path, "file": str(number), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
            elif source.exists():
                raise ValueError("Transition source is not a file: " + path)
        (stage / "manifest.json").write_text(json.dumps({"schema": 1, "entries": entries}))
        os.replace(str(stage), str(folder))
    finally:
        if stage.exists():
            shutil.rmtree(str(stage))


def verify(folder):
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("Invalid transition directory")
    document = json.loads((folder / "manifest.json").read_text())
    if document.get("schema") != 1:
        raise ValueError("Unknown transition record")
    seen = set()
    for entry in document["entries"]:
        path = entry["path"]
        if path not in FILES or path in seen:
            raise ValueError("Invalid transition path")
        seen.add(path)
        if "link" in entry:
            if not isinstance(entry["link"], str):
                raise ValueError("Invalid link")
        else:
            name = entry["file"]
            source = folder / name
            if not name.isdigit() or source.is_symlink() or not source.is_file():
                raise ValueError("Invalid transition source")
            if hashlib.sha256(source.read_bytes()).hexdigest() != entry["sha256"]:
                raise ValueError("Transition checksum mismatch")
    return document


def restore(root="/"):
    folder = local(root, STATE)
    if not folder.exists() and not folder.is_symlink():
        return
    document = verify(folder)
    # Validate the complete snapshot before replacing any destination.
    for entry in document["entries"]:
        target = local(root, entry["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        handle, name = tempfile.mkstemp(prefix=".warder-restore-", dir=str(target.parent))
        os.close(handle)
        temporary = Path(name)
        try:
            if "link" in entry:
                temporary.unlink()
                os.symlink(entry["link"], str(temporary))
            else:
                shutil.copy2(str(folder / entry["file"]), str(temporary))
            os.replace(str(temporary), str(target))
        finally:
            if temporary.exists() or temporary.is_symlink():
                temporary.unlink()
    shutil.rmtree(str(folder))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("backup", "restore"))
    args = parser.parse_args()
    (backup if args.action == "backup" else restore)()

