"""New setup strings; resolve the active OSD language on every screen opening."""
import gettext
from functools import lru_cache
from pathlib import Path
from Components.config import config


TEXT = {
    "sk": {
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Nastavenie skinu FullHDGlass",
        "Back": "Naspäť",
        "Confirm selection": "Potvrdiť výber",
        "Choose with OK": "Vybrať s OK",
        "Type": "Typ",
        "Confirm": "Potvrdiť",
        "Install 7zip from the Download menu, then retry the selected download.": "Nainštalujte 7zip z Ponuky sťahovania a potom spustite vybrané sťahovanie znova."
    },
    "cs": {
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Nastavení skinu FullHDGlass",
        "Back": "Zpět",
        "Confirm selection": "Potvrdit výběr",
        "Choose with OK": "Vybrat s OK",
        "Type": "Typ",
        "Confirm": "Potvrdit",
        "Install 7zip from the Download menu, then retry the selected download.": "Nainstalujte 7zip z Nabídky stahování a potom spusťte vybrané stahování znovu."
    },
    "de": {
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "FullHDGlass-Skin einrichten",
        "Back": "Zurück",
        "Confirm selection": "Auswahl bestätigen",
        "Choose with OK": "Mit OK auswählen",
        "Type": "Typ",
        "Confirm": "Bestätigen"
    },
    "hu": {
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "FullHDGlass felület beállítása",
        "Back": "Vissza",
        "Confirm selection": "Kiválasztás megerősítése",
        "Choose with OK": "Kiválasztás az OK gombbal",
        "Type": "Típus",
        "Confirm": "Megerősítés"
    },
    "ru": {
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Настройка скина FullHDGlass",
        "Back": "Назад",
        "Confirm selection": "Подтвердить выбор",
        "Choose with OK": "Выбрать кнопкой OK",
        "Type": "Тип",
        "Confirm": "Подтвердить"
    },
    "fr": {
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Configurer le thème FullHDGlass",
        "Back": "Retour",
        "Confirm selection": "Confirmer la sélection",
        "Choose with OK": "Choisir avec OK",
        "Type": "Type",
        "Confirm": "Confirmer"
    },
    "it": {
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Configura il tema FullHDGlass",
        "Back": "Indietro",
        "Confirm selection": "Conferma selezione",
        "Choose with OK": "Seleziona con OK",
        "Type": "Tipo",
        "Confirm": "Conferma"
    },
    "es": {
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Configurar el tema FullHDGlass",
        "Back": "Atrás",
        "Confirm selection": "Confirmar selección",
        "Choose with OK": "Seleccionar con OK",
        "Type": "Tipo",
        "Confirm": "Confirmar"
    },
    "pl": {
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Ustawienia skórki FullHDGlass",
        "Back": "Wstecz",
        "Confirm selection": "Potwierdź wybór",
        "Choose with OK": "Wybierz przyciskiem OK",
        "Type": "Typ",
        "Confirm": "Potwierdź"
    },
    "en": {
        "FullHDGlass configuration": "FullHDGlass Warder Evolution"
    }
}

for _lang, _message in {'sk': '7zip nie je dostupný pre architektúru tohto prijímača.', 'cs': '7zip není dostupný pro architekturu tohoto přijímače.', 'de': '7zip ist für die Architektur dieses Receivers nicht verfügbar.', 'hu': 'A 7zip nem érhető el ehhez a vevőarchitektúrához.', 'ru': '7zip недоступен для архитектуры этого ресивера.', 'fr': '7zip n’est pas disponible pour l’architecture de ce récepteur.', 'it': '7zip non è disponibile per l’architettura di questo ricevitore.', 'es': '7zip no está disponible para la arquitectura de este receptor.', 'pl': '7zip jest niedostępny dla architektury tego odbiornika.'}.items():
    TEXT[_lang]["7zip is not available for this receiver architecture."] = _message


@lru_cache(maxsize=24)
def _catalog(lang):
    return gettext.translation("setupGlass17", str(Path(__file__).parent / "locale"), languages=[lang], fallback=True)


def ui_text(text):
    lang = config.osd.language.value.split("_")[0].lower()
    if text in TEXT.get(lang, {}):
        return TEXT[lang][text]
    if text == "FullHDGlass configuration":
        return TEXT["en"][text]
    return _catalog(lang).gettext(text)

# Prefix for the current settings summary below the shared header.
for _lang, _selection in {'sk': 'Máš zvolené', 'cs': 'Máš zvoleno', 'en': 'Selected settings', 'de': 'Ausgewählt', 'pl': 'Wybrane ustawienia', 'hu': 'Kiválasztva', 'ru': 'Выбрано', 'fr': 'Sélection actuelle', 'it': 'Selezione attuale', 'es': 'Selección actual'}.items():
    TEXT[_lang]["Selected settings"] = _selection

# Radio header follows the same active-OSD translation resolver as settings.
for _lang, _radio_mode in {'al': 'Mënyra radio', 'cs': 'Režim rádia', 'de': 'Radiomodus', 'en': 'Radio mode', 'es': 'Modo radio', 'et': 'Raadiorežiim', 'fa': 'حالت رادیو', 'fr': 'Mode radio', 'hu': 'Rádió üzemmód', 'it': 'Modalità radio', 'lt': 'Radijo režimas', 'nl': 'Radiomodus', 'pl': 'Tryb radia', 'pt': 'Modo rádio', 'ro': 'Mod radio', 'ru': 'Режим радио', 'sk': 'Režim rádia', 'tr': 'Radyo modu', 'uk': 'Режим радіо', 'zh': '收音机模式'}.items():
    TEXT.setdefault(_lang, {})["Radio mode"] = _radio_mode

# Native caption stays translatable; the approved bitmap contains only DAB+.
for _lang, _dab_information in {'al': 'Informacione DAB+', 'cs': 'DAB+ informace', 'de': 'DAB+ Informationen', 'en': 'DAB+ information', 'es': 'Información DAB+', 'et': 'DAB+ teave', 'fa': 'اطلاعات DAB+', 'fr': 'Informations DAB+', 'hu': 'DAB+ információk', 'it': 'Informazioni DAB+', 'lt': 'DAB+ informacija', 'nl': 'DAB+ informatie', 'pl': 'Informacje DAB+', 'pt': 'Informações DAB+', 'ro': 'Informații DAB+', 'ru': 'Информация DAB+', 'sk': 'DAB+ informácie', 'tr': 'DAB+ bilgileri', 'uk': 'Інформація DAB+', 'zh': 'DAB+ 信息'}.items():
    TEXT.setdefault(_lang, {})["DAB+ information"] = _dab_information
