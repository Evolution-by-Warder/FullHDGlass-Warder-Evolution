# -*- coding: utf-8 -*-
"""Read-only user channel-picon source, separate from Warder download storage."""
import os


def normalized_directory(path):
    if not isinstance(path, str) or not path.strip():
        return ""
    path = path.strip()
    if not os.path.isabs(path) or "\x00" in path:
        return ""
    # Do not create, move, rename or remove files in the user's picon folder.
    return os.path.normpath(path)


def selected_source(config):
    """Return (override_enabled, source_directory).

    An enabled but unavailable user directory remains an override, preventing
    accidental substitution of Warder picons from another directory.
    """
    try:
        settings = config.plugins.warderUserPicons
        if settings.enabled.value:
            return True, normalized_directory(settings.path.value)
    except (AttributeError, TypeError, ValueError):
        pass
    try:
        expert = config.plugins.warderPiconExpert
        if expert.custom_destination.value:
            return True, normalized_directory(expert.destination.value)
    except (AttributeError, TypeError, ValueError):
        pass
    return False, ""


def custom_folder(config):
    enabled, path = selected_source(config)
    # Empty string means: override active, but invalid/missing path.
    # Consumers must check selected_source() to distinguish disabled mode.
    return path if enabled else None


def find_png(directory, name):
    if not directory or not os.path.isdir(directory):
        return ""
    if not isinstance(name, str) or not name or "/" in name or "\\" in name:
        return ""
    filename = os.path.join(directory, name + ".png")
    return filename if os.path.isfile(filename) else ""
