"""Conservative storage guard: /media/usb may be on receiver internal flash."""
import os

_VOLATILE = ('/tmp', '/run', '/dev', '/proc', '/sys')
_INTERNAL_SOURCES = ('/dev/mmcblk', '/dev/mtd', '/dev/ubiblock', '/dev/ubi')
# Always leave room for receiver services, logs and configuration writes.
MIN_FREE_RESERVE = 64 * 1024 * 1024

def _mount_records(mountinfo='/proc/self/mountinfo'):
    try:
        with open(mountinfo, encoding='utf-8') as file:
            for line in file:
                left, right = line.strip().split(' - ', 1)
                mount = left.split()[4].replace('\\040', ' ')
                rest = right.split()
                if len(rest) >= 2:
                    yield mount, rest[0].lower(), rest[1].lower()
    except (OSError, ValueError, IndexError):
        return

def is_internal(path, mountinfo='/proc/self/mountinfo'):
    """Warn for internal flash, unmounted media paths, or uncertain storage."""
    if not isinstance(path, str) or not path.startswith('/'):
        return True
    normalized = os.path.realpath(path)
    if normalized == '/' or any(normalized == s or normalized.startswith(s + '/') for s in _VOLATILE):
        return True
    mounts = [(mount, fs, source) for mount, fs, source in _mount_records(mountinfo)
              if normalized == mount or normalized.startswith(mount.rstrip('/') + '/')]
    if mounts:
        mount, fstype, source = max(mounts, key=lambda item: len(item[0]))
        if mount == '/' or fstype in ('tmpfs', 'ramfs', 'overlay', 'squashfs', 'ubifs', 'jffs2'):
            return True
        if source.startswith(_INTERNAL_SOURCES):
            return True
        if fstype in ('nfs', 'nfs4', 'cifs', 'smb3', 'fuse.sshfs'):
            return False
        if source.startswith('/dev/sd') or source.startswith('/dev/nvme'):
            return False
        if mount not in ('/', '/proc', '/sys'):
            try:
                return os.stat(mount).st_dev == os.stat('/').st_dev
            except OSError:
                return True
    return True

def available_bytes(path):
    """Free bytes on actual filesystem, including when target is not created."""
    if not isinstance(path, str) or not os.path.isabs(path):
        return 0
    parent = os.path.realpath(path)
    while not os.path.exists(parent) and parent != '/':
        parent = os.path.dirname(parent)
    try:
        st = os.statvfs(parent)
        return st.f_bavail * st.f_frsize
    except OSError:
        return 0


def has_space(path, additional_bytes=0, reserve=MIN_FREE_RESERVE):
    """Fail closed if enough usable bytes cannot be verified on the real target."""
    try:
        needed = int(additional_bytes)
        return needed >= 0 and available_bytes(path) >= needed + int(reserve)
    except (TypeError, ValueError, OverflowError):
        return False
