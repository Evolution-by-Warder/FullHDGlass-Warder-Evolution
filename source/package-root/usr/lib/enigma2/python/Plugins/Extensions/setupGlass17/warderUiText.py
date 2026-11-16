"""New setup strings; resolve the active OSD language on every screen opening."""
import gettext
from functools import lru_cache
from pathlib import Path
from Components.config import config


TEXT = {
    "sk": {
        "FullHDGlass skin storage": "Úložisko skinu FullHDGlass",
        "Channel-list picon source": "Zdroj piconov v zozname staníc",
        "System setting": "Systémové nastavenie",
        "Prefer 50x30": "Preferovať 50×30",
        "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.": "Systémové nastavenie zachová pôvodné vyhľadávanie piconov podľa image. Preferovať 50×30 použije picon_50x30 a chýbajúce logo doplní z picon. Uložte a reštartujte GUI.",
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
        "FullHDGlass skin storage": "Úložiště skinu FullHDGlass",
        "Channel-list picon source": "Zdroj piconů v seznamu stanic",
        "System setting": "Systémové nastavení",
        "Prefer 50x30": "Preferovat 50×30",
        "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.": "Systémové nastavení zachová původní vyhledávání piconů podle image. Preferovat 50×30 použije picon_50x30 a chybějící logo doplní z picon. Uložte a restartujte GUI.",
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
        "FullHDGlass skin storage": "FullHDGlass-Skin-Speicher",
        "Channel-list picon source": "Picon-Quelle der Senderliste",
        "System setting": "Systemeinstellung",
        "Prefer 50x30": "50×30 bevorzugen",
        "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.": "Die Systemeinstellung erhält die ursprüngliche Picon-Suche des Images. 50×30 bevorzugen nutzt picon_50x30 und ersetzt fehlende Logos aus picon. Speichern und GUI neu starten.",
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "FullHDGlass-Skin einrichten",
        "Back": "Zurück",
        "Confirm selection": "Auswahl bestätigen",
        "Choose with OK": "Mit OK auswählen",
        "Type": "Typ",
        "Confirm": "Bestätigen"
    },
    "hu": {
        "FullHDGlass skin storage": "FullHDGlass skin tárhelye",
        "Channel-list picon source": "Csatornalista piconforrása",
        "System setting": "Rendszerbeállítás",
        "Prefer 50x30": "50×30 előnyben",
        "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.": "A rendszerbeállítás megtartja az image eredeti piconkeresését. Az 50×30 mód a picon_50x30 mappát használja, hiányzó logónál a picon mappát. Ments és indítsd újra a GUI-t.",
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "FullHDGlass felület beállítása",
        "Back": "Vissza",
        "Confirm selection": "Kiválasztás megerősítése",
        "Choose with OK": "Kiválasztás az OK gombbal",
        "Type": "Típus",
        "Confirm": "Megerősítés"
    },
    "ru": {
        "FullHDGlass skin storage": "Хранилище скина FullHDGlass",
        "Channel-list picon source": "Источник пиконов списка каналов",
        "System setting": "Системная настройка",
        "Prefer 50x30": "Предпочитать 50×30",
        "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.": "Системная настройка сохраняет исходный поиск пиконов образа. Режим 50×30 использует picon_50x30, а для отсутствующих логотипов — picon. Сохраните и перезапустите GUI.",
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Настройка скина FullHDGlass",
        "Back": "Назад",
        "Confirm selection": "Подтвердить выбор",
        "Choose with OK": "Выбрать кнопкой OK",
        "Type": "Тип",
        "Confirm": "Подтвердить"
    },
    "fr": {
        "FullHDGlass skin storage": "Stockage du skin FullHDGlass",
        "Channel-list picon source": "Source des picons de la liste",
        "System setting": "Réglage système",
        "Prefer 50x30": "Préférer 50×30",
        "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.": "Le réglage système conserve la recherche de picons de l’image. Préférer 50×30 utilise picon_50x30, puis picon pour chaque logo absent. Enregistrez et redémarrez l’interface.",
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Configurer le thème FullHDGlass",
        "Back": "Retour",
        "Confirm selection": "Confirmer la sélection",
        "Choose with OK": "Choisir avec OK",
        "Type": "Type",
        "Confirm": "Confirmer"
    },
    "it": {
        "FullHDGlass skin storage": "Archivio dello skin FullHDGlass",
        "Channel-list picon source": "Origine picon nell’elenco canali",
        "System setting": "Impostazione di sistema",
        "Prefer 50x30": "Preferisci 50×30",
        "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.": "L’impostazione di sistema mantiene la ricerca originale dei picon. Preferisci 50×30 usa picon_50x30, poi picon per ogni logo mancante. Salvare e riavviare la GUI.",
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Configura il tema FullHDGlass",
        "Back": "Indietro",
        "Confirm selection": "Conferma selezione",
        "Choose with OK": "Seleziona con OK",
        "Type": "Tipo",
        "Confirm": "Conferma"
    },
    "es": {
        "FullHDGlass skin storage": "Almacenamiento del skin FullHDGlass",
        "Channel-list picon source": "Origen de picons de la lista",
        "System setting": "Ajuste del sistema",
        "Prefer 50x30": "Preferir 50×30",
        "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.": "El ajuste del sistema conserva la búsqueda original de picons. Preferir 50×30 utiliza picon_50x30 y después picon para los logos ausentes. Guarde y reinicie la interfaz.",
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Configurar el tema FullHDGlass",
        "Back": "Atrás",
        "Confirm selection": "Confirmar selección",
        "Choose with OK": "Seleccionar con OK",
        "Type": "Tipo",
        "Confirm": "Confirmar"
    },
    "pl": {
        "FullHDGlass skin storage": "Magazyn skina FullHDGlass",
        "Channel-list picon source": "Źródło piconów na liście kanałów",
        "System setting": "Ustawienie systemowe",
        "Prefer 50x30": "Preferuj 50×30",
        "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.": "Ustawienie systemowe zachowuje oryginalne wyszukiwanie piconów. Preferuj 50×30 używa picon_50x30, a brakujące ikony pobiera z picon. Zapisz i uruchom ponownie GUI.",
        "FullHDGlass configuration": "FullHDGlass Warder Evolution",
        "Configure the FullHDGlass skin": "Ustawienia skórki FullHDGlass",
        "Back": "Wstecz",
        "Confirm selection": "Potwierdź wybór",
        "Choose with OK": "Wybierz przyciskiem OK",
        "Type": "Typ",
        "Confirm": "Potwierdź"
    },
    "en": {
        "FullHDGlass skin storage": "FullHDGlass skin storage",
        "Channel-list picon source": "Channel-list picon source",
        "System setting": "System setting",
        "Prefer 50x30": "Prefer 50x30",
        "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.": "System setting keeps the image's original picon lookup. Prefer 50x30 uses picon_50x30, then picon for each missing logo. Save and restart the GUI.",
        "FullHDGlass configuration": "FullHDGlass Warder Evolution"
    }
}

for _lang, _message in {'sk': '7zip nie je dostupný pre architektúru tohto prijímača.', 'cs': '7zip není dostupný pro architekturu tohoto přijímače.', 'de': '7zip ist für die Architektur dieses Receivers nicht verfügbar.', 'hu': 'A 7zip nem érhető el ehhez a vevőarchitektúrához.', 'ru': '7zip недоступен для архитектуры этого ресивера.', 'fr': '7zip n’est pas disponible pour l’architecture de ce récepteur.', 'it': '7zip non è disponibile per l’architettura di questo ricevitore.', 'es': '7zip no está disponible para la arquitectura de este receptor.', 'pl': '7zip jest niedostępny dla architektury tego odbiornika.'}.items():
    TEXT[_lang]["7zip is not available for this receiver architecture."] = _message


# Expert picon selector uses the active system language.
TEXT.setdefault("sk", {})["Custom picon location"] = "Vlastné umiestnenie piconov"
TEXT.setdefault("cs", {})["Custom picon location"] = "Vlastní umístění piconů"
TEXT.setdefault("de", {})["Custom picon location"] = "Benutzerdefinierter Picon-Speicherort"
TEXT.setdefault("en", {})["Custom picon location"] = "Custom picon location"
TEXT.setdefault("pl", {})["Custom picon location"] = "Własna lokalizacja pikon"
TEXT.setdefault("hu", {})["Custom picon location"] = "Egyéni piconhely"
TEXT.setdefault("ru", {})["Custom picon location"] = "Своё расположение пиконов"
TEXT.setdefault("fr", {})["Custom picon location"] = "Emplacement personnalisé des picons"
TEXT.setdefault("it", {})["Custom picon location"] = "Posizione personalizzata dei picon"
TEXT.setdefault("es", {})["Custom picon location"] = "Ubicación personalizada de picons"
TEXT.setdefault("al", {})["Custom picon location"] = "Vendndodhja e personalizuar e piconëve"
TEXT.setdefault("el", {})["Custom picon location"] = "Προσαρμοσμένη θέση picon"
TEXT.setdefault("et", {})["Custom picon location"] = "Kohandatud piconite asukoht"
TEXT.setdefault("fa", {})["Custom picon location"] = "مسیر دلخواه پیکون‌ها"
TEXT.setdefault("lt", {})["Custom picon location"] = "Pasirinktinė pikonų vieta"
TEXT.setdefault("nl", {})["Custom picon location"] = "Aangepaste piconlocatie"
TEXT.setdefault("pt", {})["Custom picon location"] = "Localização personalizada dos picons"
TEXT.setdefault("ro", {})["Custom picon location"] = "Locație personalizată pentru piconuri"
TEXT.setdefault("tr", {})["Custom picon location"] = "Özel picon konumu"
TEXT.setdefault("uk", {})["Custom picon location"] = "Власне розташування піктограм"
TEXT.setdefault("zh", {})["Custom picon location"] = "自定义台标位置"

# Destination menu follows the current Enigma2 OSD language in all 21 supported locales.
TEXT.setdefault("al", {})["FullHDGlass skin storage"] = "Hapësira e skin-it FullHDGlass"
TEXT.setdefault("el", {})["FullHDGlass skin storage"] = "Αποθήκευση του skin FullHDGlass"
TEXT.setdefault("et", {})["FullHDGlass skin storage"] = "FullHDGlassi kujunduse salvestuskoht"
TEXT.setdefault("fa", {})["FullHDGlass skin storage"] = "فضای ذخیره‌سازی پوسته FullHDGlass"
TEXT.setdefault("lt", {})["FullHDGlass skin storage"] = "FullHDGlass apvalkalo saugykla"
TEXT.setdefault("nl", {})["FullHDGlass skin storage"] = "FullHDGlass-skinopslag"
TEXT.setdefault("pt", {})["FullHDGlass skin storage"] = "Armazenamento do skin FullHDGlass"
TEXT.setdefault("ro", {})["FullHDGlass skin storage"] = "Spațiul de stocare al temei FullHDGlass"
TEXT.setdefault("tr", {})["FullHDGlass skin storage"] = "FullHDGlass tema depolama alanı"
TEXT.setdefault("uk", {})["FullHDGlass skin storage"] = "Сховище скіна FullHDGlass"
TEXT.setdefault("zh", {})["FullHDGlass skin storage"] = "FullHDGlass 皮肤存储位置"

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

# Spinner names and help use the active environment language. Author nicknames
# remain literal in the catalog.
for _lang, (_dove, _help, _error) in {
    'al': ('Pëllumbi', 'Zgjidh animacionin e pritjes. Ruaje për ta zbatuar pas rinisjes së GUI.', 'Animacioni nuk mund të ndryshohej. Skedarët ekzistues u ruajtën.'),
    'cs': ('Holubice', 'Vyberte animaci čekání. Po uložení se použije po restartu GUI.', 'Animaci se nepodařilo změnit. Vaše původní soubory zůstaly zachovány.'),
    'de': ('Taube', 'Wählen Sie die Warteanimation. Nach dem Speichern wird sie beim GUI-Neustart aktiviert.', 'Die Animation konnte nicht geändert werden. Ihre bisherigen Dateien wurden beibehalten.'),
    'en': ('Dove', 'Choose the waiting animation. Save to apply it after a GUI restart.', 'The spinner could not be changed. Your existing files were preserved.'),
    'es': ('Paloma', 'Elija la animación de espera. Guarde para aplicarla tras reiniciar la interfaz.', 'No se pudo cambiar la animación. Se conservaron sus archivos existentes.'),
    'et': ('Tuvi', 'Valige ooteanimatsioon. Pärast salvestamist rakendub see kasutajaliidese taaskäivitamisel.', 'Animatsiooni ei saanud muuta. Olemasolevad failid säilitati.'),
    'fa': ('کبوتر', 'پویانمایی انتظار را انتخاب کنید. پس از ذخیره و راه‌اندازی مجدد رابط اعمال می‌شود.', 'تغییر پویانمایی ممکن نشد. پرونده‌های موجود شما حفظ شدند.'),
    'fr': ('Colombe', 'Choisissez l’animation d’attente. Enregistrez pour l’appliquer au redémarrage de l’interface.', 'L’animation n’a pas pu être modifiée. Vos fichiers existants ont été conservés.'),
    'hu': ('Galamb', 'Válassza ki a várakozási animációt. Mentés után a kezelőfelület újraindításakor lép életbe.', 'Az animáció nem módosítható. A meglévő fájlok megmaradtak.'),
    'it': ('Colomba', 'Scegli l’animazione di attesa. Salva per applicarla dopo il riavvio dell’interfaccia.', 'Impossibile cambiare l’animazione. I file esistenti sono stati conservati.'),
    'lt': ('Balandis', 'Pasirinkite laukimo animaciją. Išsaugojus ji bus pritaikyta paleidus sąsają iš naujo.', 'Animacijos pakeisti nepavyko. Esami failai išsaugoti.'),
    'nl': ('Duif', 'Kies de wachtanimatie. Sla op om deze na een GUI-herstart toe te passen.', 'De animatie kon niet worden gewijzigd. Uw bestaande bestanden zijn behouden.'),
    'pl': ('Gołąb', 'Wybierz animację oczekiwania. Po zapisaniu zostanie zastosowana po restarcie GUI.', 'Nie udało się zmienić animacji. Dotychczasowe pliki zostały zachowane.'),
    'pt': ('Pomba', 'Escolha a animação de espera. Guarde para aplicar após reiniciar a interface.', 'Não foi possível alterar a animação. Os ficheiros existentes foram preservados.'),
    'ro': ('Porumbel', 'Alegeți animația de așteptare. Salvați pentru a o aplica după repornirea interfeței.', 'Animația nu a putut fi schimbată. Fișierele existente au fost păstrate.'),
    'ru': ('Голубь', 'Выберите анимацию ожидания. Сохраните для применения после перезапуска интерфейса.', 'Не удалось изменить анимацию. Ваши существующие файлы сохранены.'),
    'sk': ('Holubica', 'Vyberte animáciu čakania. Po uložení sa použije po reštarte GUI.', 'Animáciu sa nepodarilo zmeniť. Vaše pôvodné súbory zostali zachované.'),
    'tr': ('Güvercin', 'Bekleme animasyonunu seçin. Kaydettikten sonra arayüz yeniden başlatıldığında uygulanır.', 'Animasyon değiştirilemedi. Mevcut dosyalarınız korundu.'),
    'uk': ('Голуб', 'Виберіть анімацію очікування. Збережіть для застосування після перезапуску інтерфейсу.', 'Не вдалося змінити анімацію. Ваші наявні файли збережено.'),
    'zh': ('鸽子', '选择等待动画。保存后将在界面重启时应用。', '无法更改等待动画。现有文件已保留。'),
}.items():
    TEXT.setdefault(_lang, {}).update({
        'Dove': _dove,
        'Choose the waiting animation. Save to apply it after a GUI restart.': _help,
        'The spinner could not be changed. Your existing files were preserved.': _error,
    })


# Native-image spinner selection, localized in all supported OSD languages.
for _lang, _title in {
    "al": "Animacioni i parazgjedhur i imazhit",
    "cs": "Výchozí spinner image",
    "de": "Standard-Spinner des Images",
    "en": "Default spinner of image",
    "es": "Animación predeterminada de la imagen",
    "et": "Image'i vaikimisi ooteanimatsioon",
    "fa": "انیمیشن پیش‌فرض ایمیج",
    "fr": "Animation d’attente par défaut de l’image",
    "hu": "Az image alapértelmezett animációja",
    "it": "Animazione predefinita dell'immagine",
    "lt": "Numatytoji imidžo animacija",
    "nl": "Standaardspinner van de image",
    "pl": "Domyślna animacja obrazu",
    "pt": "Animação predefinida da imagem",
    "ro": "Animația implicită a imaginii",
    "ru": "Спиннер по умолчанию из имиджа",
    "sk": "Predvolený spinner image",
    "tr": "İmajın varsayılan bekleme animasyonu",
    "uk": "Стандартний спінер іміджу",
    "zh": "系统镜像默认等待动画"
}.items():
    TEXT.setdefault(_lang, {})['Default spinner of image'] = _title

# On-demand spinner selection status follows the active OSD language.
for _lang, _values in {'sk': ['Načítavam zoznam spinnerov…', 'Online zoznam je nedostupný. Nainštalované spinnery sú k dispozícii.', 'Sťahujem vybraný spinner…', 'Spinner sa nepodarilo stiahnuť. Skúste znova.'], 'cs': ['Načítám seznam spinnerů…', 'Online seznam je nedostupný. Nainstalované spinnery jsou k dispozici.', 'Stahuji vybraný spinner…', 'Spinner se nepodařilo stáhnout. Zkuste znovu.'], 'de': ['Spinner-Liste wird geladen…', 'Online-Liste nicht verfügbar. Installierte Spinner sind verfügbar.', 'Gewählter Spinner wird geladen…', 'Spinner konnte nicht geladen werden. Erneut versuchen.'], 'en': ['Loading spinner list...', 'Online list unavailable. Installed spinners are available.', 'Downloading selected spinner...', 'Spinner download failed. Try again.'], 'pl': ['Wczytywanie listy animacji…', 'Lista online jest niedostępna. Zainstalowane animacje są dostępne.', 'Pobieranie wybranej animacji…', 'Nie udało się pobrać animacji. Spróbuj ponownie.'], 'hu': ['Animációlista betöltése…', 'Az online lista nem érhető el. A telepített animációk elérhetők.', 'A kiválasztott animáció letöltése…', 'Az animáció letöltése sikertelen. Próbálja újra.'], 'ru': ['Загрузка списка анимаций…', 'Онлайн-список недоступен. Установленные анимации доступны.', 'Загрузка выбранной анимации…', 'Не удалось загрузить анимацию. Повторите попытку.'], 'fr': ['Chargement des animations…', 'Liste en ligne indisponible. Les animations installées restent disponibles.', 'Téléchargement de l’animation choisie…', 'Échec du téléchargement. Réessayez.'], 'it': ['Caricamento delle animazioni…', 'Elenco online non disponibile. Le animazioni installate sono disponibili.', 'Download dell’animazione selezionata…', 'Download non riuscito. Riprova.'], 'es': ['Cargando animaciones…', 'Lista en línea no disponible. Las animaciones instaladas están disponibles.', 'Descargando la animación seleccionada…', 'No se pudo descargar. Inténtalo de nuevo.'], 'pt': ['A carregar animações…', 'Lista online indisponível. As animações instaladas estão disponíveis.', 'A transferir a animação selecionada…', 'Não foi possível transferir. Tente novamente.'], 'nl': ['Animatielijst laden…', 'Onlinelijst niet beschikbaar. Geïnstalleerde animaties zijn beschikbaar.', 'Geselecteerde animatie downloaden…', 'Download mislukt. Probeer opnieuw.'], 'ro': ['Se încarcă animațiile…', 'Lista online nu este disponibilă. Animațiile instalate sunt disponibile.', 'Se descarcă animația aleasă…', 'Descărcarea a eșuat. Încercați din nou.'], 'uk': ['Завантаження списку анімацій…', 'Онлайн-список недоступний. Установлені анімації доступні.', 'Завантаження вибраної анімації…', 'Не вдалося завантажити. Спробуйте ще раз.'], 'lt': ['Įkeliamas animacijų sąrašas…', 'Internetinis sąrašas nepasiekiamas. Įdiegtos animacijos pasiekiamos.', 'Atsisiunčiama pasirinkta animacija…', 'Atsisiųsti nepavyko. Bandykite dar kartą.'], 'et': ['Animatsioonide loendi laadimine…', 'Veebiloend pole saadaval. Paigaldatud animatsioonid on saadaval.', 'Valitud animatsiooni allalaadimine…', 'Allalaadimine ebaõnnestus. Proovige uuesti.'], 'al': ['Duke ngarkuar animacionet…', 'Lista në internet nuk është e disponueshme. Animacionet e instaluara janë të disponueshme.', 'Duke shkarkuar animacionin e zgjedhur…', 'Shkarkimi dështoi. Provo sërish.'], 'tr': ['Animasyon listesi yükleniyor…', 'Çevrimiçi liste kullanılamıyor. Yüklü animasyonlar kullanılabilir.', 'Seçilen animasyon indiriliyor…', 'İndirme başarısız. Yeniden deneyin.'], 'fa': ['در حال بارگیری فهرست پویانمایی\u200cها…', 'فهرست آنلاین در دسترس نیست. پویانمایی\u200cهای نصب\u200cشده در دسترس هستند.', 'در حال دریافت پویانمایی انتخاب\u200cشده…', 'دریافت ناموفق بود. دوباره تلاش کنید.'], 'zh': ['正在加载动画列表…', '在线列表不可用。仍可使用已安装的动画。', '正在下载所选动画…', '下载失败，请重试。']}.items():
    TEXT.setdefault(_lang, {}).update(dict(zip(['Loading spinner list...', 'Online list unavailable. Installed spinners are available.', 'Downloading selected spinner...', 'Spinner download failed. Try again.'], _values)))


# Storage location includes graphics sets, picons and other downloaded skin data.
for _lang, _label in {
    "sk": "Úložisko grafických sád, piconov a dát",
    "cs": "Úložiště grafických sad, piconů a dat",
    "de": "Speicherort für Grafiksets, Picons und Daten",
    "hu": "Grafikai csomagok, piconok és adatok tárhelye",
    "ru": "Хранилище графических наборов, пиконов и данных",
    "fr": "Stockage des packs graphiques, picons et données",
    "it": "Archivio set grafici, picon e dati",
    "es": "Almacenamiento de conjuntos gráficos, picons y datos",
    "pl": "Magazyn zestawów graficznych, pikonów i danych",
    "en": "Storage for graphics sets, picons and data",
    "pt": "Armazenamento de conjuntos gráficos, picons e dados",
    "nl": "Opslag voor grafische sets, picons en gegevens",
    "ro": "Stocare seturi grafice, piconuri și date",
    "uk": "Сховище графічних наборів, піконів і даних",
    "lt": "Grafikos rinkinių, pikonų ir duomenų saugykla",
    "et": "Graafikakomplektide, pikonite ja andmete salvestus",
    "al": "Ruajtja e paketave grafike, pikonëve dhe të dhënave",
    "tr": "Grafik setleri, piconlar ve veri depolama",
    "fa": "محل ذخیره بسته‌های گرافیکی، پیکون‌ها و داده‌ها",
    "zh": "图形套件、台标和数据存储位置",
}.items():
    TEXT.setdefault(_lang, {})["Storage for graphics sets, picons and data"] = _label

# Short help for the PATHS storage setting, localized at runtime.
for _lang, _text in {
    "sk": "Úložisko stiahnutých grafických sád, piconov a ďalších dát skinu. Po uložení zmeny cesty sa tu vytvorí hdg17_files.",
    "cs": "Úložiště stažených grafických sad, piconů a dalších dat skinu. Po uložení změny cesty se zde vytvoří hdg17_files.",
    "de": "Speicherort für heruntergeladene Grafiksets, Picons und weitere Skin-Daten. Nach dem Speichern eines geänderten Pfads wird hier hdg17_files erstellt.",
    "en": "Storage for downloaded graphics sets, picons and other skin data. Saving a changed path creates hdg17_files here.",
    "pl": "Miejsce na pobrane zestawy grafik, pikony i inne dane skórki. Po zapisaniu zmiany ścieżki powstanie tu hdg17_files.",
    "hu": "Letöltött grafikai készletek, piconok és egyéb skinadatok helye. A módosított útvonal mentésekor itt jön létre a hdg17_files.",
    "ru": "Хранилище загруженных наборов графики, пиконов и других данных скина. При сохранении нового пути здесь создаётся hdg17_files.",
    "fr": "Emplacement des packs graphiques, picons et autres données téléchargées du skin. L'enregistrement d'un nouveau chemin crée ici hdg17_files.",
    "it": "Percorso per set grafici, picon e altri dati scaricati della skin. Salvando un percorso modificato viene creata qui hdg17_files.",
    "es": "Ubicación de conjuntos gráficos, picons y otros datos descargados del skin. Al guardar una ruta modificada se crea aquí hdg17_files.",
    "pt": "Local para conjuntos gráficos, picons e outros dados descarregados da skin. Ao guardar uma alteração de caminho, cria-se aqui hdg17_files.",
    "nl": "Opslag voor gedownloade grafische sets, picons en andere skingegevens. Bij het opslaan van een gewijzigd pad wordt hier hdg17_files gemaakt.",
    "ro": "Loc pentru seturi grafice, piconuri și alte date descărcate ale skinului. Salvarea căii modificate creează aici hdg17_files.",
    "uk": "Сховище завантажених графічних наборів, піконів та інших даних скіна. Після збереження зміненого шляху тут створюється hdg17_files.",
    "lt": "Vieta atsisiųstiems grafikos rinkiniams, pikonams ir kitiems apvalkalo duomenims. Išsaugojus pakeistą kelią čia sukuriamas hdg17_files.",
    "et": "Allalaaditud graafikakomplektide, pikonite ja muude kujundusandmete asukoht. Muudetud tee salvestamisel luuakse siia hdg17_files.",
    "al": "Vend për paketat grafike, pikonët dhe të dhëna të tjera të shkarkuara të skin-it. Ruajtja e rrugës së ndryshuar krijon këtu hdg17_files.",
    "tr": "İndirilen grafik setleri, piconlar ve diğer tema verileri için depolama. Yol değişikliği kaydedilince burada hdg17_files oluşturulur.",
    "fa": "محل نگهداری مجموعه‌های گرافیکی، پیکون‌ها و دیگر داده‌های دانلودشده پوسته. با ذخیره مسیر تغییر‌یافته، پوشه hdg17_files اینجا ساخته می‌شود.",
    "zh": "用于存储下载的图形套件、台标及其他皮肤数据。保存更改后的路径时会在此创建 hdg17_files。",
}.items():
    TEXT.setdefault(_lang, {})["Storage for downloaded graphics sets, picons and other skin data. Saving a changed path creates hdg17_files here."] = _text

# Separate help for the FHDG backup configuration file setting.
for _lang, _text in {
    "sk": "Tu si zvolíte adresár, do ktorého sa bude ukladať záložný konfiguračný súbor hdg17.conf. Predvolené umiestnenie je /usr/share/enigma2/hd_glass17/. Stlačením OK môžete vybrať iný adresár a tlačidlom SAVE zálohu uložiť.",
    "cs": "Zde vyberete adresář pro záložní konfigurační soubor hdg17.conf. Výchozí umístění je /usr/share/enigma2/hd_glass17/. Stisknutím OK lze vybrat jiný adresář a tlačítkem SAVE zálohu uložit.",
    "en": "Choose where to save the backup configuration file hdg17.conf. Default: /usr/share/enigma2/hd_glass17/. Press OK to choose another folder, then SAVE to save the backup.",
    "de": "Wählen Sie den Ordner für die Sicherung der Konfigurationsdatei hdg17.conf. Standard: /usr/share/enigma2/hd_glass17/. Mit OK einen anderen Ordner wählen und mit SAVE die Sicherung speichern.",
    "pl": "Wybierz folder dla kopii zapasowej pliku konfiguracji hdg17.conf. Domyślnie: /usr/share/enigma2/hd_glass17/. Naciśnij OK, aby wybrać inny folder, a następnie SAVE, aby zapisać kopię.",
    "hu": "Itt választható ki a hdg17.conf biztonsági konfigurációs fájl mappája. Alapértelmezett: /usr/share/enigma2/hd_glass17/. OK: másik mappa; SAVE: mentés.",
    "ru": "Выберите папку для резервного файла конфигурации hdg17.conf. По умолчанию: /usr/share/enigma2/hd_glass17/. Нажмите OK для выбора другой папки, затем SAVE для сохранения копии.",
    "fr": "Choisissez le dossier de sauvegarde du fichier de configuration hdg17.conf. Par défaut : /usr/share/enigma2/hd_glass17/. Appuyez sur OK pour choisir un autre dossier, puis sur SAVE pour sauvegarder.",
    "it": "Scegli la cartella per il file di configurazione di backup hdg17.conf. Predefinita: /usr/share/enigma2/hd_glass17/. Premi OK per scegliere un'altra cartella e SAVE per salvare il backup.",
    "es": "Elija la carpeta para la copia de seguridad de configuración hdg17.conf. Predeterminada: /usr/share/enigma2/hd_glass17/. Pulse OK para elegir otra carpeta y SAVE para guardar la copia.",
    "pt": "Escolha a pasta para a cópia de segurança do ficheiro de configuração hdg17.conf. Padrão: /usr/share/enigma2/hd_glass17/. Prima OK para outra pasta e SAVE para guardar.",
    "nl": "Kies de map voor het reserveconfiguratiebestand hdg17.conf. Standaard: /usr/share/enigma2/hd_glass17/. Druk op OK om een andere map te kiezen en op SAVE om de back-up op te slaan.",
    "ro": "Alegeți dosarul pentru copia de rezervă a fișierului de configurare hdg17.conf. Implicit: /usr/share/enigma2/hd_glass17/. Apăsați OK pentru alt dosar și SAVE pentru a salva copia.",
    "uk": "Виберіть теку для резервного файлу конфігурації hdg17.conf. Типово: /usr/share/enigma2/hd_glass17/. Натисніть OK для вибору іншої теки, потім SAVE для збереження копії.",
    "lt": "Pasirinkite aplanką atsarginei hdg17.conf konfigūracijos kopijai. Numatytasis: /usr/share/enigma2/hd_glass17/. Spauskite OK kitam aplankui pasirinkti, tada SAVE kopijai įrašyti.",
    "et": "Valige kaust varukoopia seadistusfailile hdg17.conf. Vaikimisi: /usr/share/enigma2/hd_glass17/. Teise kausta valimiseks vajutage OK, salvestamiseks SAVE.",
    "al": "Zgjidhni dosjen për skedarin rezervë të konfigurimit hdg17.conf. Parazgjedhja: /usr/share/enigma2/hd_glass17/. Shtypni OK për dosje tjetër, pastaj SAVE për ta ruajtur.",
    "tr": "Yedek yapılandırma dosyası hdg17.conf için klasör seçin. Varsayılan: /usr/share/enigma2/hd_glass17/. Başka klasör için OK, yedeği kaydetmek için SAVE tuşuna basın.",
    "fa": "پوشه ذخیره نسخه پشتیبان تنظیمات hdg17.conf را انتخاب کنید. مسیر پیش‌فرض: /usr/share/enigma2/hd_glass17/. برای انتخاب پوشه دیگر OK و برای ذخیره نسخه پشتیبان SAVE را بزنید.",
    "zh": "选择配置备份文件 hdg17.conf 的保存文件夹。默认位置：/usr/share/enigma2/hd_glass17/。按 OK 选择其他文件夹，再按 SAVE 保存备份。",
}.items():
    TEXT.setdefault(_lang, {})["Choose where to save the backup configuration file hdg17.conf. Default: /usr/share/enigma2/hd_glass17/. Press OK to choose another folder, then SAVE to save the backup."] = _text

# Factory icon restore failure, translated for active OSD language.
for _lang, _text in {
    "sk": "Nepodarilo sa obnoviť základné ikony. Preinštalujte skin.",
    "cs": "Nepodařilo se obnovit základní ikony. Přeinstalujte skin.",
    "en": "Unable to restore bundled default icons. Please reinstall the skin.",
    "de": "Die Standard-Icons konnten nicht wiederhergestellt werden. Bitte den Skin neu installieren.",
    "pl": "Nie udało się przywrócić domyślnych ikon. Zainstaluj skórkę ponownie.",
    "hu": "Az alapértelmezett ikonok visszaállítása sikertelen. Telepítse újra a skint.",
    "ru": "Не удалось восстановить стандартные значки. Переустановите скин.",
    "fr": "Impossible de restaurer les icônes d'origine. Réinstallez le skin.",
    "it": "Impossibile ripristinare le icone predefinite. Reinstalla la skin.",
    "es": "No se pudieron restaurar los iconos originales. Reinstala el skin.",
    "pt": "Não foi possível restaurar os ícones padrão. Reinstale a skin.",
    "nl": "Standaardpictogrammen konden niet worden hersteld. Installeer de skin opnieuw.",
    "ro": "Pictogramele implicite nu au putut fi restaurate. Reinstalați skinul.",
    "uk": "Не вдалося відновити стандартні значки. Перевстановіть скін.",
    "lt": "Nepavyko atkurti numatytųjų piktogramų. Įdiekite apvalkalą iš naujo.",
    "et": "Vaikimisi ikoonide taastamine ebaõnnestus. Paigaldage kujundus uuesti.",
    "al": "Ikonat e parazgjedhura nuk u rikthyen. Riinstaloni skin-in.",
    "tr": "Varsayılan simgeler geri yüklenemedi. Temayı yeniden yükleyin.",
    "fa": "بازیابی نمادهای پیش‌فرض ممکن نشد. پوسته را دوباره نصب کنید.",
    "zh": "无法恢复默认图标，请重新安装皮肤。",
}.items():
    TEXT.setdefault(_lang, {})["Unable to restore bundled default icons. Please reinstall the skin."] = _text

# Clear storage-path menu title in all supported OSD languages.
TEXT.setdefault("sk", {})["Paths for Skin Data, Picons and Settings"] = "Cesty k dátam skinu, piconom a nastaveniam"
TEXT.setdefault("cs", {})["Paths for Skin Data, Picons and Settings"] = "Cesty k datům skinu, piconům a nastavení"
TEXT.setdefault("de", {})["Paths for Skin Data, Picons and Settings"] = "Pfade für Skin-Daten, Picons und Einstellungen"
TEXT.setdefault("hu", {})["Paths for Skin Data, Picons and Settings"] = "Skinadatok, piconok és beállítások útvonalai"
TEXT.setdefault("ru", {})["Paths for Skin Data, Picons and Settings"] = "Пути к данным скина, пиконам и настройкам"
TEXT.setdefault("fr", {})["Paths for Skin Data, Picons and Settings"] = "Chemins des données, picons et réglages"
TEXT.setdefault("it", {})["Paths for Skin Data, Picons and Settings"] = "Percorsi per dati skin, picon e impostazioni"
TEXT.setdefault("es", {})["Paths for Skin Data, Picons and Settings"] = "Rutas de datos, picons y ajustes"
TEXT.setdefault("pl", {})["Paths for Skin Data, Picons and Settings"] = "Ścieżki danych skórki, pikon i ustawień"
TEXT.setdefault("en", {})["Paths for Skin Data, Picons and Settings"] = "Paths for Skin Data, Picons and Settings"
TEXT.setdefault("al", {})["Paths for Skin Data, Picons and Settings"] = "Shtigjet e të dhënave, piconëve dhe cilësimeve"
TEXT.setdefault("el", {})["Paths for Skin Data, Picons and Settings"] = "Διαδρομές δεδομένων, picons και ρυθμίσεων"
TEXT.setdefault("et", {})["Paths for Skin Data, Picons and Settings"] = "Kujunduse andmete, piconide ja seadete teed"
TEXT.setdefault("fa", {})["Paths for Skin Data, Picons and Settings"] = "مسیر داده‌های پوسته، پیکون‌ها و تنظیمات"
TEXT.setdefault("lt", {})["Paths for Skin Data, Picons and Settings"] = "Apvalkalo duomenų, pikonų ir nustatymų keliai"
TEXT.setdefault("nl", {})["Paths for Skin Data, Picons and Settings"] = "Paden voor skingegevens, picons en instellingen"
TEXT.setdefault("pt", {})["Paths for Skin Data, Picons and Settings"] = "Caminhos de dados, picons e definições"
TEXT.setdefault("ro", {})["Paths for Skin Data, Picons and Settings"] = "Căi pentru datele skinului, piconuri și setări"
TEXT.setdefault("tr", {})["Paths for Skin Data, Picons and Settings"] = "Skin verileri, piconlar ve ayar yolları"
TEXT.setdefault("uk", {})["Paths for Skin Data, Picons and Settings"] = "Шляхи до даних скіна, піктограм і налаштувань"
TEXT.setdefault("zh", {})["Paths for Skin Data, Picons and Settings"] = "皮肤数据、台标和设置路径"

# Source-only channel-picon override, independent of all download destinations.
TEXT.setdefault("sk", {})["Use own channel picons"] = "Vlastné picony staníc"
TEXT.setdefault("sk", {})["Own picon folder"] = "Priečinok vlastných piconov"
TEXT.setdefault("sk", {})["Selected picon folder does not exist."] = "Vybraný priečinok piconov neexistuje."
TEXT.setdefault("cs", {})["Use own channel picons"] = "Vlastní picony stanic"
TEXT.setdefault("cs", {})["Own picon folder"] = "Složka vlastních piconů"
TEXT.setdefault("cs", {})["Selected picon folder does not exist."] = "Vybraná složka piconů neexistuje."
TEXT.setdefault("en", {})["Use own channel picons"] = "Use own channel picons"
TEXT.setdefault("en", {})["Own picon folder"] = "Own picon folder"
TEXT.setdefault("en", {})["Selected picon folder does not exist."] = "Selected picon folder does not exist."
TEXT.setdefault("de", {})["Use own channel picons"] = "Eigene Sender-Picons"
TEXT.setdefault("de", {})["Own picon folder"] = "Eigener Picon-Ordner"
TEXT.setdefault("de", {})["Selected picon folder does not exist."] = "Der gewählte Picon-Ordner existiert nicht."
TEXT.setdefault("pl", {})["Use own channel picons"] = "Własne pikony kanałów"
TEXT.setdefault("pl", {})["Own picon folder"] = "Folder własnych pikon"
TEXT.setdefault("pl", {})["Selected picon folder does not exist."] = "Wybrany folder pikon nie istnieje."
TEXT.setdefault("hu", {})["Use own channel picons"] = "Saját csatornapikonok"
TEXT.setdefault("hu", {})["Own picon folder"] = "Saját pikonmappa"
TEXT.setdefault("hu", {})["Selected picon folder does not exist."] = "A kiválasztott pikonmappa nem létezik."
TEXT.setdefault("fr", {})["Use own channel picons"] = "Picons de chaînes perso"
TEXT.setdefault("fr", {})["Own picon folder"] = "Dossier des picons perso"
TEXT.setdefault("fr", {})["Selected picon folder does not exist."] = "Le dossier de picons sélectionné est introuvable."
TEXT.setdefault("it", {})["Use own channel picons"] = "Picon canali personali"
TEXT.setdefault("it", {})["Own picon folder"] = "Cartella picon personali"
TEXT.setdefault("it", {})["Selected picon folder does not exist."] = "La cartella picon selezionata non esiste."
TEXT.setdefault("es", {})["Use own channel picons"] = "Piconos propios de canal"
TEXT.setdefault("es", {})["Own picon folder"] = "Carpeta de piconos propios"
TEXT.setdefault("es", {})["Selected picon folder does not exist."] = "La carpeta de piconos seleccionada no existe."
TEXT.setdefault("pt", {})["Use own channel picons"] = "Picons de canais próprios"
TEXT.setdefault("pt", {})["Own picon folder"] = "Pasta dos picons próprios"
TEXT.setdefault("pt", {})["Selected picon folder does not exist."] = "A pasta de picons selecionada não existe."
TEXT.setdefault("nl", {})["Use own channel picons"] = "Eigen zenderpicons"
TEXT.setdefault("nl", {})["Own picon folder"] = "Map eigen picons"
TEXT.setdefault("nl", {})["Selected picon folder does not exist."] = "De gekozen piconmap bestaat niet."
TEXT.setdefault("ro", {})["Use own channel picons"] = "Piconuri proprii canale"
TEXT.setdefault("ro", {})["Own picon folder"] = "Folder piconuri proprii"
TEXT.setdefault("ro", {})["Selected picon folder does not exist."] = "Folderul de piconuri selectat nu există."
TEXT.setdefault("ru", {})["Use own channel picons"] = "Свои пиконы каналов"
TEXT.setdefault("ru", {})["Own picon folder"] = "Папка своих пиконов"
TEXT.setdefault("ru", {})["Selected picon folder does not exist."] = "Выбранная папка пиконов не существует."
TEXT.setdefault("uk", {})["Use own channel picons"] = "Власні пікони каналів"
TEXT.setdefault("uk", {})["Own picon folder"] = "Тека власних піконів"
TEXT.setdefault("uk", {})["Selected picon folder does not exist."] = "Вибраної теки піконів не існує."
TEXT.setdefault("tr", {})["Use own channel picons"] = "Özel kanal piconları"
TEXT.setdefault("tr", {})["Own picon folder"] = "Özel picon klasörü"
TEXT.setdefault("tr", {})["Selected picon folder does not exist."] = "Seçilen picon klasörü mevcut değil."
TEXT.setdefault("zh", {})["Use own channel picons"] = "使用自定义频道台标"
TEXT.setdefault("zh", {})["Own picon folder"] = "自定义台标目录"
TEXT.setdefault("zh", {})["Selected picon folder does not exist."] = "所选台标目录不存在。"
TEXT.setdefault("lt", {})["Use own channel picons"] = "Savi kanalų pikonai"
TEXT.setdefault("lt", {})["Own picon folder"] = "Savų pikonų aplankas"
TEXT.setdefault("lt", {})["Selected picon folder does not exist."] = "Pasirinkto pikonų aplanko nėra."
TEXT.setdefault("et", {})["Use own channel picons"] = "Oma kanalipikonid"
TEXT.setdefault("et", {})["Own picon folder"] = "Oma pikonite kaust"
TEXT.setdefault("et", {})["Selected picon folder does not exist."] = "Valitud pikonikausta pole olemas."
TEXT.setdefault("al", {})["Use own channel picons"] = "Pikonet personale"
TEXT.setdefault("al", {})["Own picon folder"] = "Dosja e pikoneve"
TEXT.setdefault("al", {})["Selected picon folder does not exist."] = "Dosja e zgjedhur e pikoneve nuk ekziston."
TEXT.setdefault("fa", {})["Use own channel picons"] = "پیکون‌های شخصی شبکه‌ها"
TEXT.setdefault("fa", {})["Own picon folder"] = "پوشه پیکون‌های شخصی"
TEXT.setdefault("fa", {})["Selected picon folder does not exist."] = "پوشه پیکون انتخاب‌شده وجود ندارد."
TEXT.setdefault("el", {})["Use own channel picons"] = "Προσωπικά picons καναλιών"
TEXT.setdefault("el", {})["Own picon folder"] = "Φάκελος προσωπικών picons"
TEXT.setdefault("el", {})["Selected picon folder does not exist."] = "Ο επιλεγμένος φάκελος picons δεν υπάρχει."

# Context help for the own-channel-picon source and read-only folder picker.
TEXT.setdefault("sk", {})["Enable this option to display your own channel picons from a selected folder. Downloads still use Warder storage; your folder is never modified."] = "Zapnutím sa budú picony staníc zobrazovať z vášho priečinka. Sťahovanie naďalej používa úložisko Warder; vaše súbory zostanú nedotknuté."
TEXT.setdefault("sk", {})["Press OK to choose a folder containing your channel picons. The skin only reads PNG files here for InfoBars and channel lists; it never downloads, changes or deletes them."] = "Stlačením OK vyberiete priečinok s vlastnými piconmi staníc. Skin odtiaľ iba číta PNG pre InfoBary a zoznam staníc. Nič nesťahuje, nemení ani nemaže."
TEXT.setdefault("cs", {})["Enable this option to display your own channel picons from a selected folder. Downloads still use Warder storage; your folder is never modified."] = "Po zapnutí se picony stanic zobrazí z vaší složky. Stahování dál používá úložiště Warder; vaše soubory zůstanou beze změny."
TEXT.setdefault("cs", {})["Press OK to choose a folder containing your channel picons. The skin only reads PNG files here for InfoBars and channel lists; it never downloads, changes or deletes them."] = "Stisknutím OK vyberete složku s vlastními picony stanic. Skin odtud pouze čte PNG pro InfoBary a seznam stanic. Nic nestahuje, nemění ani nemaže."
TEXT.setdefault("de", {})["Enable this option to display your own channel picons from a selected folder. Downloads still use Warder storage; your folder is never modified."] = "Aktivieren Sie eigene Sender-Picons aus einem gewählten Ordner. Downloads bleiben im Warder-Speicher; Ihre Dateien werden nicht verändert."
TEXT.setdefault("de", {})["Press OK to choose a folder containing your channel picons. The skin only reads PNG files here for InfoBars and channel lists; it never downloads, changes or deletes them."] = "Mit OK wählen Sie den Ordner Ihrer Sender-Picons. Der Skin liest dort nur PNG-Dateien für InfoBars und Senderlisten; er verändert oder löscht nichts."
TEXT.setdefault("pl", {})["Enable this option to display your own channel picons from a selected folder. Downloads still use Warder storage; your folder is never modified."] = "Włącz własne pikony kanałów z wybranego folderu. Pobieranie nadal korzysta z pamięci Warder; Twoje pliki pozostaną bez zmian."
TEXT.setdefault("pl", {})["Press OK to choose a folder containing your channel picons. The skin only reads PNG files here for InfoBars and channel lists; it never downloads, changes or deletes them."] = "Naciśnij OK, aby wybrać folder z własnymi pikonami. Skórka tylko odczytuje PNG dla pasków informacji i list kanałów, niczego nie usuwa ani nie zmienia."
TEXT.setdefault("hu", {})["Enable this option to display your own channel picons from a selected folder. Downloads still use Warder storage; your folder is never modified."] = "Engedélyezze saját csatornapikonjait egy kiválasztott mappából. A letöltések a Warder tárhelyét használják; fájljai érintetlenek maradnak."
TEXT.setdefault("hu", {})["Press OK to choose a folder containing your channel picons. The skin only reads PNG files here for InfoBars and channel lists; it never downloads, changes or deletes them."] = "Nyomjon OK-t a pikonmappa kiválasztásához. A felület csak olvassa az InfoBarok és csatornalisták PNG fájljait, nem módosít és nem töröl."
TEXT.setdefault("fr", {})["Enable this option to display your own channel picons from a selected folder. Downloads still use Warder storage; your folder is never modified."] = "Activez les picons de chaînes de votre dossier. Les téléchargements restent dans le stockage Warder et vos fichiers ne sont jamais modifiés."
TEXT.setdefault("fr", {})["Press OK to choose a folder containing your channel picons. The skin only reads PNG files here for InfoBars and channel lists; it never downloads, changes or deletes them."] = "Appuyez sur OK pour choisir le dossier des picons. Le skin lit seulement les PNG pour les InfoBars et listes de chaînes, sans les modifier ni les supprimer."
TEXT.setdefault("it", {})["Enable this option to display your own channel picons from a selected folder. Downloads still use Warder storage; your folder is never modified."] = "Attiva i picon personali dalla cartella scelta. I download rimangono nell'archivio Warder e i tuoi file non vengono modificati."
TEXT.setdefault("it", {})["Press OK to choose a folder containing your channel picons. The skin only reads PNG files here for InfoBars and channel lists; it never downloads, changes or deletes them."] = "Premi OK per scegliere la cartella dei picon. La skin legge soltanto i PNG per InfoBar ed elenchi canali, senza modificarli o eliminarli."
TEXT.setdefault("es", {})["Enable this option to display your own channel picons from a selected folder. Downloads still use Warder storage; your folder is never modified."] = "Active sus propios piconos desde una carpeta elegida. Las descargas siguen usando el almacén Warder y no se modifican sus archivos."
TEXT.setdefault("es", {})["Press OK to choose a folder containing your channel picons. The skin only reads PNG files here for InfoBars and channel lists; it never downloads, changes or deletes them."] = "Pulse OK para elegir la carpeta de piconos. El skin solo lee PNG para InfoBars y listas de canales; no modifica ni elimina archivos."
TEXT.setdefault("en", {})["Enable this option to display your own channel picons from a selected folder. Downloads still use Warder storage; your folder is never modified."] = "Enable this option to display your own channel picons from a selected folder. Downloads still use Warder storage; your folder is never modified."
TEXT.setdefault("en", {})["Press OK to choose a folder containing your channel picons. The skin only reads PNG files here for InfoBars and channel lists; it never downloads, changes or deletes them."] = "Press OK to choose a folder containing your channel picons. The skin only reads PNG files here for InfoBars and channel lists; it never downloads, changes or deletes them."
