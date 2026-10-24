"""New setup strings; resolve the active OSD language on every screen opening."""
import gettext
from functools import lru_cache
from pathlib import Path
from Components.config import config


TEXT = {
    "sk": {
        "FullHDGlass configuration": "Konfigurácia FullHDGlass",
        "Configure the FullHDGlass skin": "Nastavenie skinu FullHDGlass",
        "Back": "Naspäť", "Confirm selection": "Potvrdiť výber", "Choose with OK": "Vybrať s OK",
        "Type": "Typ", "Confirm": "Potvrdiť",
        "Install 7zip from the Download menu, then retry the selected download.": "Nainštalujte 7zip z Ponuky sťahovania a potom spustite vybrané sťahovanie znova.",
    },
    "cs": {
        "FullHDGlass configuration": "Konfigurace FullHDGlass",
        "Configure the FullHDGlass skin": "Nastavení skinu FullHDGlass",
        "Back": "Zpět", "Confirm selection": "Potvrdit výběr", "Choose with OK": "Vybrat s OK",
        "Type": "Typ", "Confirm": "Potvrdit",
        "Install 7zip from the Download menu, then retry the selected download.": "Nainstalujte 7zip z Nabídky stahování a potom spusťte vybrané stahování znovu.",
    },
    "de": {"FullHDGlass configuration": "FullHDGlass-Konfiguration", "Configure the FullHDGlass skin": "FullHDGlass-Skin einrichten", "Back": "Zurück", "Confirm selection": "Auswahl bestätigen", "Choose with OK": "Mit OK auswählen", "Type": "Typ", "Confirm": "Bestätigen"},
    "hu": {"FullHDGlass configuration": "FullHDGlass beállítások", "Configure the FullHDGlass skin": "FullHDGlass felület beállítása", "Back": "Vissza", "Confirm selection": "Kiválasztás megerősítése", "Choose with OK": "Kiválasztás az OK gombbal", "Type": "Típus", "Confirm": "Megerősítés"},
    "ru": {"FullHDGlass configuration": "Настройка FullHDGlass", "Configure the FullHDGlass skin": "Настройка скина FullHDGlass", "Back": "Назад", "Confirm selection": "Подтвердить выбор", "Choose with OK": "Выбрать кнопкой OK", "Type": "Тип", "Confirm": "Подтвердить"},
    "fr": {"FullHDGlass configuration": "Configuration FullHDGlass", "Configure the FullHDGlass skin": "Configurer le thème FullHDGlass", "Back": "Retour", "Confirm selection": "Confirmer la sélection", "Choose with OK": "Choisir avec OK", "Type": "Type", "Confirm": "Confirmer"},
    "it": {"FullHDGlass configuration": "Configurazione FullHDGlass", "Configure the FullHDGlass skin": "Configura il tema FullHDGlass", "Back": "Indietro", "Confirm selection": "Conferma selezione", "Choose with OK": "Seleziona con OK", "Type": "Tipo", "Confirm": "Conferma"},
    "es": {"FullHDGlass configuration": "Configuración FullHDGlass", "Configure the FullHDGlass skin": "Configurar el tema FullHDGlass", "Back": "Atrás", "Confirm selection": "Confirmar selección", "Choose with OK": "Seleccionar con OK", "Type": "Tipo", "Confirm": "Confirmar"},
    "pl": {"FullHDGlass configuration": "Konfiguracja FullHDGlass", "Configure the FullHDGlass skin": "Ustawienia skórki FullHDGlass", "Back": "Wstecz", "Confirm selection": "Potwierdź wybór", "Choose with OK": "Wybierz przyciskiem OK", "Type": "Typ", "Confirm": "Potwierdź"},
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
    return _catalog(lang).gettext(text)
