"""Runtime gettext resolver shared by FullHDGlass setup, weather and help.

Resolve Enigma2 language variants and request the selected catalog in the
background. English source text is available while the catalog is absent.
"""
from collections.abc import Mapping
from functools import lru_cache
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
_watched_language = None

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
    if code == "en":
        return
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


def watch_language(config, plugin_dir):
    """Schedule the selected language at startup and on every OSD language change."""
    global _watched_language

    def changed(setting):
        request_language(language_code(setting.value), plugin_dir)

    setting = getattr(getattr(config, "osd", None), "language", None)
    if setting is not _watched_language and hasattr(setting, "addNotifier"):
        setting.addNotifier(changed, initial_call=True)
        _watched_language = setting

    # FullHDGlass uses large native setup labels. Keep translated text away
    # from native slider/value columns without touching compact dialogs.
    if getattr(getattr(getattr(config, "skin", None), "primary_skin", None), "value", None) == "hd_glass17/skin.xml":
        try:
            from .warderNativeConfigSpacing import install as install_native_spacing
            install_native_spacing()
        except (ImportError, AttributeError):
            pass


def get_translator(domain, config, plugin_dir, *, always_osd=False):
    """Look up messages in the current language, refreshing after an atomic download."""
    checked_until = 0
    current = None
    translate = identity

    def active_catalog():
        nonlocal checked_until, current, translate
        try:
            code = language_code(config.osd.language.value)
            if not always_osd and not config.plugins.setupGlass17.par49.value:
                code = "en"
        except (AttributeError, TypeError, ValueError):
            code = "en"
        now = time.monotonic()
        if current and current[0] == code and now < checked_until:
            return translate
        checked_until = now + 2
        if code == "en":
            current = (code, None)
            translate = identity
            return translate

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
        return translate

    def lookup(message):
        return active_catalog()(message)

    lookup.active_catalog = active_catalog
    return lookup


class TranslatedMapping(Mapping):
    """Cache a translated table until its catalog or the OSD language changes."""
    def __init__(self, translator, make_table):
        self._active = translator.active_catalog
        self._table = lru_cache(maxsize=1)(make_table)

    def __getitem__(self, key):
        return self._table(self._active())[key]

    def __iter__(self):
        return iter(self._table(self._active()))

    def __len__(self):
        return len(self._table(self._active()))


def _load(domain, code, downloaded, plugin_dir):
    if downloaded:
        try:
            with open(downloaded, "rb") as stream:
                return gettext.GNUTranslations(stream).gettext
        except (OSError, ValueError, EOFError, IndexError, LookupError, struct.error):
            pass
    try:
        return gettext.translation(
            domain, localedir=os.path.join(plugin_dir, "locale"),
            languages=[code], fallback=True
        ).gettext
    except (OSError, ValueError, EOFError, IndexError, LookupError, struct.error):
        return identity
