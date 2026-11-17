"""Runtime gettext resolver shared by FullHDGlass setup, weather and help.

Resolve Enigma2 language variants; return English source text if a .mo
catalog is absent. This module never downloads or generates translations.
"""
import gettext
import os

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


def get_translator(domain, config, plugin_dir):
    """Respect the skin translation setting; missing catalogs are harmless."""
    try:
        if not config.plugins.setupGlass17.par49.value:
            return identity
        code = language_code(config.osd.language.value)
        if code == "en":
            return identity
        return gettext.translation(
            domain, localedir=os.path.join(plugin_dir, "locale"),
            languages=[code], fallback=True
        ).gettext
    except (AttributeError, OSError, TypeError, ValueError):
        return identity
