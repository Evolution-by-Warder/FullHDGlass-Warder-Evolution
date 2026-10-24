"""Resolve the private helper first, then image-provided 7zip executables."""
import os
import shutil


def find_sevenzip(private_path):
    candidates = [private_path]
    candidates.extend(shutil.which(name) for name in ("7zz", "7z", "7za"))
    return next((path for path in candidates if path and os.path.isfile(path) and os.access(path, os.X_OK)), None)
