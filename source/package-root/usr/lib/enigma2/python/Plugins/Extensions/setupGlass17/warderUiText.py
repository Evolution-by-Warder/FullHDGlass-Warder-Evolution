"""Resolve setup and information-screen labels in the active OSD language."""
from pathlib import Path

from Components.config import config
from .warderLocale import get_translator

_translate = get_translator("setupGlass17", config, str(Path(__file__).parent), always_osd=True)
_ENGLISH_LABELS = {
    "FullHDGlass configuration": "FullHDGlass Warder Evolution",
    "Internal storage download warning": "Warning! Download to internal storage",
}


def ui_text(text):
    translated = _translate(text)
    if translated == text:
        return _ENGLISH_LABELS.get(text, text)
    return translated
