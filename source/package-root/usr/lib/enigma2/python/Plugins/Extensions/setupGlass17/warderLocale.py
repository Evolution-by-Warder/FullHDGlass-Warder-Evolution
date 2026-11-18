"""Runtime gettext resolver shared by FullHDGlass setup, weather and help.

Resolve Enigma2 language variants; return English source text if a .mo
catalog is absent. This module never downloads or generates translations.
"""
import gettext
import os
import subprocess
import sys

LANGUAGES = ("al", "cs", "de", "el", "en", "es", "et", "fa", "fr", "hu",
             "it", "lt", "nl", "pl", "pt", "ro", "ru", "sk", "tr", "uk", "zh")
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


def request_missing_language(code, plugin_dir):
    """Start an independent fetch process at most once per language per boot.

    Never block the GUI and never delete a previously downloaded language.
    Failures are tolerated; the next reboot permits retry.
    """
    if code == "en":
        return
    helper = os.path.join(plugin_dir, "warderLocaleDownload.py")
    manifest = os.path.join(plugin_dir, "warder-locale-manifest.json")
    if not (os.path.isfile(helper) and os.path.isfile(manifest)):
        return
    marker = "/tmp/warder-locale-request-" + code
    try:
        fd = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except OSError:
        return
    os.close(fd)
    try:
        with open(os.devnull, "wb") as devnull:
            subprocess.Popen(
                [sys.executable, "-B", helper, "--language", code],
                stdin=devnull, stdout=devnull, stderr=devnull,
                close_fds=True, start_new_session=True,
            )
    except OSError:
        try:
            os.unlink(marker)
        except OSError:
            pass


def get_translator(domain, config, plugin_dir):
    """Respect the skin translation setting; missing catalogs are harmless."""
    try:
        if not config.plugins.setupGlass17.par49.value:
            return identity
        code = language_code(config.osd.language.value)
        if code == "en":
            return identity
        catalog = os.path.join(plugin_dir, "locale", code, "LC_MESSAGES", domain + ".mo")
        if not os.path.isfile(catalog):
            request_missing_language(code, plugin_dir)
        return gettext.translation(
            domain, localedir=os.path.join(plugin_dir, "locale"),
            languages=[code], fallback=True
        ).gettext
    except (AttributeError, OSError, TypeError, ValueError):
        return identity
