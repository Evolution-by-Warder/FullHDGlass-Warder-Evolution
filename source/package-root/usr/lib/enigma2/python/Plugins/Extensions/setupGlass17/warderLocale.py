"""Runtime gettext resolver shared by FullHDGlass setup, weather and help.

Resolve Enigma2 language variants and request the selected catalog in the
background. English source text is available while the catalog is absent.
"""
import gettext
import os
import subprocess
import struct
import sys
import time

from .warderLocaleDownload import LOCALE as DOWNLOADED_LOCALE

LANGUAGES = ("al", "cs", "de", "el", "en", "es", "et", "fa", "fr", "hu",
             "it", "lt", "nl", "pl", "pt", "ro", "ru", "sk", "tr", "uk", "zh")
_last_request = {}

ALIASES = {"sq": "al", "gr": "el", "cz": "cs", "ua": "uk", "cn": "zh"}


def language_code(value):
    try:
        code = str(value or "en").replace("-", "_").split("_", 1)[0].lower()
    except (TypeError, ValueError):
        return "en"
    code = ALIASES.get(code, code)
    return code if code in LANGUAGES else "en"


def identity(message):
    return message


def request_language(code, plugin_dir):
    """Start a background sync with a retry interval for offline receivers."""
    helper = os.path.join(plugin_dir, "warderLocaleDownload.py")
    manifest = os.path.join(plugin_dir, "warder-locale-manifest.json")
    if not (os.path.isfile(helper) and os.path.isfile(manifest)):
        return
    now = time.monotonic()
    if now < _last_request.get(code, 0):
        return
    _last_request[code] = now + 300
    try:
        with open(os.devnull, "wb") as devnull:
            subprocess.Popen(
                [sys.executable, "-B", helper, "--language", code],
                stdin=devnull, stdout=devnull, stderr=devnull,
                close_fds=True, start_new_session=True,
            )
    except OSError:
        pass


def get_translator(domain, config, plugin_dir):
    """Follow downloaded catalogs without repeatedly reading them from disk."""
    checked_until = 0
    current = None
    translate = identity

    def lookup(message):
        nonlocal checked_until, current, translate
        now = time.monotonic()
        if now < checked_until:
            return translate(message)
        checked_until = now + 2
        try:
            if not config.plugins.setupGlass17.par49.value:
                code = "en"
            else:
                code = language_code(config.osd.language.value)
        except (AttributeError, TypeError, ValueError):
            code = "en"
        if code == "en":
            current = None
            translate = identity
            return message

        request_language(code, plugin_dir)
        downloaded = os.path.join(DOWNLOADED_LOCALE, code, "LC_MESSAGES", domain + ".mo")
        try:
            info = os.stat(downloaded)
            stamp = (info.st_ino, info.st_mtime_ns, info.st_size)
        except OSError:
            stamp = None
        if current != (code, stamp):
            translate = _load(domain, code, downloaded if stamp else None, plugin_dir)
            current = (code, stamp)
        return translate(message)

    return lookup


def _load(domain, code, downloaded, plugin_dir):
    if downloaded:
        try:
            with open(downloaded, "rb") as stream:
                return gettext.GNUTranslations(stream).gettext
        except (OSError, ValueError, EOFError, struct.error):
            pass
    try:
        return gettext.translation(
            domain, localedir=os.path.join(plugin_dir, "locale"),
            languages=[code], fallback=True
        ).gettext
    except (OSError, ValueError, EOFError, struct.error):
        return identity
