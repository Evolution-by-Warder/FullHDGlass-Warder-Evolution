"""Small self-contained translations; UI language follows the receiver."""
try:
    from Components.Language import language
    LANG = language.getLanguage()[:2]
except (ImportError, AttributeError):
    LANG = 'en'

SK = {
    'Radio stations': 'Rádiá', 'Favourites': 'Obľúbené', 'History': 'História',
    'Recordings': 'Nahrávky', 'Settings': 'Nastavenia', 'Close': 'Zavrieť',
    'Play': 'Prehrať', 'Stop': 'Zastaviť', 'Search': 'Vyhľadať', 'Favourite': 'Obľúbené',
    'Now playing': 'Práve hrá', 'Ready to listen': 'Pripravené na počúvanie',
    'Select a station and press OK': 'Vyberte stanicu a stlačte OK',
    'No stations': 'Žiadne stanice', 'No recordings': 'Žiadne nahrávky',
    'No track information': 'Stanica neposkytuje informácie o skladbe',
    'Connecting…': 'Pripájam…', 'Playing': 'Prehrávam', 'Stopped': 'Zastavené',
    'Playback ended': 'Prehrávanie sa skončilo', 'All groups': 'Všetky skupiny',
    'Choose group': 'Vybrať skupinu', 'Update catalogue': 'Aktualizovať katalóg',
    'Add station': 'Pridať vlastnú stanicu', 'Station name': 'Názov stanice',
    'Stream URL': 'Adresa streamu', 'Search all stations': 'Vyhľadávanie vo všetkých staniciach',
    'Catalogue updated': 'Katalóg bol aktualizovaný', 'Updating catalogue…': 'Aktualizujem katalóg…',
    'Saved': 'Uložené', 'Removed from favourites': 'Odstránené z obľúbených',
    'Added to favourites': 'Pridané do obľúbených', 'Cannot save settings': 'Nastavenia sa nepodarilo uložiť',
    'Cannot update catalogue': 'Katalóg sa nepodarilo aktualizovať',
    'Cannot play station': 'Stanicu sa nepodarilo spustiť',
    'Start recording': 'Spustiť nahrávanie', 'Stop recording': 'Zastaviť nahrávanie',
    'Recording started': 'Nahrávanie sa spustilo', 'Recording stopped': 'Nahrávanie sa zastavilo',
    'Recording requires streamripper': 'Na nahrávanie nainštalujte doplnok streamripper.',
    'Recording requires a mounted disk': 'Na nahrávanie je potrebný pripojený disk /media/hdd.',
    'Recording failed': 'Nahrávanie zlyhalo', 'Recordings folder': 'Priečinok nahrávok',
    'About': 'O plugine', 'Playback activity': 'Aktivita prehrávania',
    'Use left/right to switch panels · MENU: options': 'Vľavo/vpravo: výber panela · MENU: možnosti',
    'Custom': 'Vlastné', 'Information': 'Informácie', 'Search results': 'Výsledky vyhľadávania',
}
CS = dict(SK, **{
    'Radio stations': 'Rádia', 'Favourites': 'Oblíbené', 'History': 'Historie',
    'Recordings': 'Nahrávky', 'Settings': 'Nastavení', 'Close': 'Zavřít',
    'Play': 'Přehrát', 'Stop': 'Zastavit', 'Search': 'Vyhledat', 'Favourite': 'Oblíbené',
    'Now playing': 'Právě hraje', 'Ready to listen': 'Připraveno k poslechu',
    'Select a station and press OK': 'Vyberte stanici a stiskněte OK',
    'No stations': 'Žádné stanice', 'No recordings': 'Žádné nahrávky',
    'No track information': 'Stanice neposkytuje informace o skladbě',
    'Connecting…': 'Připojuji…', 'Playing': 'Přehrávám', 'Stopped': 'Zastaveno',
    'Playback ended': 'Přehrávání skončilo', 'All groups': 'Všechny skupiny',
    'Choose group': 'Vybrat skupinu', 'Update catalogue': 'Aktualizovat katalog',
    'Add station': 'Přidat vlastní stanici', 'Station name': 'Název stanice',
    'Stream URL': 'Adresa streamu', 'Search all stations': 'Vyhledávání ve všech stanicích',
    'Catalogue updated': 'Katalog byl aktualizován', 'Updating catalogue…': 'Aktualizuji katalog…',
    'Saved': 'Uloženo', 'Removed from favourites': 'Odstraněno z oblíbených',
    'Added to favourites': 'Přidáno do oblíbených', 'Cannot save settings': 'Nastavení se nepodařilo uložit',
    'Cannot update catalogue': 'Katalog se nepodařilo aktualizovat',
    'Cannot play station': 'Stanici se nepodařilo spustit',
    'Start recording': 'Spustit nahrávání', 'Stop recording': 'Zastavit nahrávání',
    'Recording started': 'Nahrávání bylo spuštěno', 'Recording stopped': 'Nahrávání bylo zastaveno',
    'Recording requires streamripper': 'Pro nahrávání nainstalujte doplněk streamripper.',
    'Recording requires a mounted disk': 'Pro nahrávání je potřebný připojený disk /media/hdd.',
    'Recording failed': 'Nahrávání selhalo', 'Recordings folder': 'Složka nahrávek',
    'About': 'O pluginu', 'Playback activity': 'Aktivita přehrávání',
    'Use left/right to switch panels · MENU: options': 'Vlevo/vpravo: výběr panelu · MENU: možnosti',
    'Custom': 'Vlastní', 'Information': 'Informace', 'Search results': 'Výsledky vyhledávání',
})


def t(text):
    return (SK if LANG == 'sk' else CS if LANG == 'cs' else {}).get(text, text)
