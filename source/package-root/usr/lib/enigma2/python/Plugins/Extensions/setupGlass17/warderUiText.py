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


# The native Channel Selection context menu has to use the receiver OSD
# language, even if the optional translation catalog is not downloaded yet.
# Keep these five new strings available offline in all 21 skin languages.
_RADIO_COUNTRY_KEYS = (
    "Select country (Warder Radio Live)",
    "(current)",
    "Country list is unavailable.",
    "Country selection could not be saved.",
    "Loading radio stations for the selected country.",
)
_RADIO_COUNTRY_TRANSLATIONS = {
    "al": ("Zgjidh vendin (Warder Radio Live)", "(aktual)", "Lista e vendeve nuk është e disponueshme.", "Zgjedhja e vendit nuk mund të ruhej.", "Po ngarkohen radiot e vendit të zgjedhur."),
    "cs": ("Vybrat zemi (Warder Radio Live)", "(aktuální)", "Seznam zemí není dostupný.", "Výběr země se nepodařilo uložit.", "Načítají se rozhlasové stanice vybrané země."),
    "de": ("Land auswählen (Warder Radio Live)", "(aktuell)", "Die Länderliste ist nicht verfügbar.", "Die Länderauswahl konnte nicht gespeichert werden.", "Radiosender des ausgewählten Landes werden geladen."),
    "el": ("Επιλογή χώρας (Warder Radio Live)", "(τρέχουσα)", "Η λίστα χωρών δεν είναι διαθέσιμη.", "Δεν ήταν δυνατή η αποθήκευση της χώρας.", "Φόρτωση σταθμών της επιλεγμένης χώρας."),
    "en": _RADIO_COUNTRY_KEYS,
    "es": ("Seleccionar país (Warder Radio Live)", "(actual)", "La lista de países no está disponible.", "No se pudo guardar la selección del país.", "Cargando emisoras del país seleccionado."),
    "et": ("Vali riik (Warder Radio Live)", "(praegune)", "Riikide loend pole saadaval.", "Riigi valikut ei saanud salvestada.", "Valitud riigi raadiojaamu laaditakse."),
    "fa": ("انتخاب کشور (Warder Radio Live)", "(فعلی)", "فهرست کشورها در دسترس نیست.", "انتخاب کشور ذخیره نشد.", "در حال بارگذاری ایستگاه‌های رادیویی کشور انتخاب‌شده."),
    "fr": ("Choisir un pays (Warder Radio Live)", "(actuel)", "La liste des pays est indisponible.", "Impossible d’enregistrer le pays sélectionné.", "Chargement des radios du pays sélectionné."),
    "hu": ("Ország kiválasztása (Warder Radio Live)", "(jelenlegi)", "Az országok listája nem érhető el.", "Az országválasztás mentése sikertelen.", "A kiválasztott ország rádióállomásainak betöltése."),
    "it": ("Seleziona paese (Warder Radio Live)", "(attuale)", "L'elenco dei paesi non è disponibile.", "Impossibile salvare il paese selezionato.", "Caricamento delle radio del paese selezionato."),
    "lt": ("Pasirinkti šalį (Warder Radio Live)", "(dabartinė)", "Šalių sąrašas nepasiekiamas.", "Nepavyko išsaugoti šalies pasirinkimo.", "Įkeliamos pasirinktos šalies radijo stotys."),
    "nl": ("Land kiezen (Warder Radio Live)", "(huidig)", "De landenlijst is niet beschikbaar.", "De landkeuze kon niet worden opgeslagen.", "Radiozenders van het gekozen land worden geladen."),
    "pl": ("Wybierz kraj (Warder Radio Live)", "(aktualny)", "Lista krajów jest niedostępna.", "Nie udało się zapisać wybranego kraju.", "Wczytywanie stacji radiowych wybranego kraju."),
    "pt": ("Selecionar país (Warder Radio Live)", "(atual)", "A lista de países não está disponível.", "Não foi possível guardar o país selecionado.", "A carregar estações do país selecionado."),
    "ro": ("Alege țara (Warder Radio Live)", "(actuală)", "Lista țărilor nu este disponibilă.", "Selecția țării nu a putut fi salvată.", "Se încarcă posturile radio din țara selectată."),
    "ru": ("Выбрать страну (Warder Radio Live)", "(текущая)", "Список стран недоступен.", "Не удалось сохранить выбор страны.", "Загружаются радиостанции выбранной страны."),
    "sk": ("Vybrať krajinu (Warder Radio Live)", "(aktuálna)", "Zoznam krajín nie je dostupný.", "Výber krajiny sa nepodarilo uložiť.", "Načítavajú sa rádiové stanice vybranej krajiny."),
    "tr": ("Ülke seç (Warder Radio Live)", "(geçerli)", "Ülke listesi kullanılamıyor.", "Ülke seçimi kaydedilemedi.", "Seçilen ülkenin radyo istasyonları yükleniyor."),
    "uk": ("Вибрати країну (Warder Radio Live)", "(поточна)", "Список країн недоступний.", "Не вдалося зберегти вибір країни.", "Завантажуються радіостанції вибраної країни."),
    "zh": ("选择国家或地区 (Warder Radio Live)", "（当前）", "国家或地区列表不可用。", "无法保存国家或地区选择。", "正在加载所选国家或地区的广播电台。"),
}


_RADIO_COUNTRY_START_ERROR = "Country saved, but background radio update did not start."
_RADIO_COUNTRY_START_ERROR_TRANSLATIONS = {
    "al": "Vendi u ruajt, por përditësimi i radios nuk u nis.",
    "cs": "Země byla uložena, ale aktualizace rádií se nespustila.",
    "de": "Land gespeichert, aber die Radioaktualisierung wurde nicht gestartet.",
    "el": "Η χώρα αποθηκεύτηκε, αλλά δεν ξεκίνησε η ενημέρωση ραδιοφώνου.",
    "en": _RADIO_COUNTRY_START_ERROR,
    "es": "País guardado, pero la actualización de radio no se inició.",
    "et": "Riik salvestati, kuid raadio värskendamine ei käivitunud.",
    "fa": "کشور ذخیره شد اما به‌روزرسانی رادیو شروع نشد.",
    "fr": "Pays enregistré, mais la mise à jour radio n'a pas démarré.",
    "hu": "Az ország mentve, de a rádiófrissítés nem indult el.",
    "it": "Paese salvato, ma l'aggiornamento radio non è partito.",
    "lt": "Šalis išsaugota, bet radijo atnaujinimas neprasidėjo.",
    "nl": "Land opgeslagen, maar de radio-update is niet gestart.",
    "pl": "Kraj zapisany, ale aktualizacja radia nie została uruchomiona.",
    "pt": "País guardado, mas a atualização da rádio não começou.",
    "ro": "Țara a fost salvată, dar actualizarea radio nu a pornit.",
    "ru": "Страна сохранена, но обновление радио не запустилось.",
    "sk": "Krajina bola uložená, ale aktualizácia rádia sa nespustila.",
    "tr": "Ülke kaydedildi, ancak radyo güncellemesi başlatılamadı.",
    "uk": "Країну збережено, але оновлення радіо не запустилося.",
    "zh": "国家或地区已保存，但广播更新未能启动。",
}


def ui_text(text):
    translated = _translate(text)
    if translated == text:
        if text == _RADIO_COUNTRY_START_ERROR:
            try:
                code = language_code(config.osd.language.value)
            except (AttributeError, TypeError, ValueError):
                code = "en"
            return _RADIO_COUNTRY_START_ERROR_TRANSLATIONS.get(code, text)
        if text in _RADIO_COUNTRY_KEYS:
            try:
                code = language_code(config.osd.language.value)
            except (AttributeError, TypeError, ValueError):
                code = "en"
            return _RADIO_COUNTRY_TRANSLATIONS.get(code, _RADIO_COUNTRY_KEYS)[
                _RADIO_COUNTRY_KEYS.index(text)]
        if text == _MAIN_MENU_KEY:
            try:
                code = language_code(config.osd.language.value)
            except (AttributeError, TypeError, ValueError):
                code = "en"
            return _MAIN_MENU_TRANSLATIONS.get(code, text)
        return _ENGLISH_LABELS.get(text, text)
    return translated
