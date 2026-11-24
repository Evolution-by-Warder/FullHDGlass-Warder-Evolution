"""Bounded, deduplicated menu artwork report; no other diagnostic logging."""
import fcntl
import os
import stat

REPORT = "/tmp/missing_menu_icons.txt"
MAX_BYTES = 256 * 1024
SKIN_IDS = ("warder_fullhdglass_settings", "FHD_Glass17_Setup")
SKIN_ART = "/usr/share/enigma2/hd_glass17/menu/warder_skin.png"

def report_missing(filename, path=None):
    # Only exact, safe filenames; empty entries and paths are not menu icons.
    if not isinstance(filename, str) or not filename.endswith(".png") or filename == ".png":
        return
    if len(filename) > 240 or any(c in filename for c in ("/", "\\", "\r", "\n", "\0")):
        return
    fd = None
    try:
        flags = os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_NONBLOCK | os.O_NOFOLLOW
        fd = os.open(path or REPORT, flags, 0o600)
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if os.fstat(fd).st_size >= MAX_BYTES:
            return
        raw = filename.encode("utf-8")
        os.lseek(fd, 0, os.SEEK_SET)
        existing = os.read(fd, MAX_BYTES)
        if raw not in existing.splitlines() and len(existing) + len(raw) + 1 <= MAX_BYTES:
            os.write(fd, raw + b"\n")
    except (OSError, UnicodeError, AttributeError):
        pass  # A reporting problem must never break the menu.
    finally:
        if fd is not None:
            os.close(fd)

def skin_artwork(entry_id, root, pict, exists):
    if entry_id not in SKIN_IDS:
        return None
    # Exact user-supplied variant takes precedence in the renderer. Then
    # reuse the approved canonical download or bundled original, never the
    # old bundled FHD_Glass17_Setup.png wrench.
    if pict:
        candidate = root + "/menuIconsBig/" + entry_id + ".png"
        if exists(candidate):
            return candidate
    candidate = root + "/menuIconsBig/FHD_Glass17_Setup.png"
    if exists(candidate):
        return candidate
    return SKIN_ART if exists(SKIN_ART) else None
