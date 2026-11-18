"""Resolve setup and information-screen labels in the active OSD language."""
from pathlib import Path

from Components.config import config
from .warderLocale import get_translator, language_code

_translate = get_translator("setupGlass17", config, str(Path(__file__).parent), always_osd=True)
_ENGLISH_LABELS = {
    "FullHDGlass configuration": "FullHDGlass Warder Evolution",
    "Internal storage download warning": "Warning! Download to internal storage",
}

_MAIN_MENU_KEY = "Show FullHDGlass Warder Evolution in main menu"
_MAIN_MENU_TRANSLATIONS = {
    "sk": "Zobraziť FullHDGlass Warder Evolution v hlavnom menu",
    "cs": "Zobrazit FullHDGlass Warder Evolution v hlavní nabídce",
    "en": "Show FullHDGlass Warder Evolution in main menu",
    "de": "FullHDGlass Warder Evolution im Hauptmenü anzeigen",
    "fr": "Afficher FullHDGlass Warder Evolution dans le menu principal",
    "es": "Mostrar FullHDGlass Warder Evolution en el menú principal",
    "it": "Mostra FullHDGlass Warder Evolution nel menu principale",
    "pt": "Mostrar FullHDGlass Warder Evolution no menu principal",
    "pl": "Pokaż FullHDGlass Warder Evolution w menu głównym",
    "hu": "FullHDGlass Warder Evolution megjelenítése a főmenüben",
    "ru": "Показывать FullHDGlass Warder Evolution в главном меню",
    "uk": "Показувати FullHDGlass Warder Evolution у головному меню",
    "ro": "Afișează FullHDGlass Warder Evolution în meniul principal",
    "nl": "FullHDGlass Warder Evolution in hoofdmenu tonen",
    "lt": "Rodyti FullHDGlass Warder Evolution pagrindiniame meniu",
    "et": "Kuva FullHDGlass Warder Evolution peamenüüs",
    "al": "Shfaq FullHDGlass Warder Evolution në menynë kryesore",
    "el": "Εμφάνιση FullHDGlass Warder Evolution στο κύριο μενού",
    "tr": "FullHDGlass Warder Evolution ana menüde gösterilsin",
    "fa": "نمایش FullHDGlass Warder Evolution در منوی اصلی",
    "zh": "在主菜单中显示 FullHDGlass Warder Evolution",
}


def ui_text(text):
    translated = _translate(text)
    if translated == text:
        if text == _MAIN_MENU_KEY:
            try:
                code = language_code(config.osd.language.value)
            except (AttributeError, TypeError, ValueError):
                code = "en"
            return _MAIN_MENU_TRANSLATIONS.get(code, text)
        return _ENGLISH_LABELS.get(text, text)
    return translated
