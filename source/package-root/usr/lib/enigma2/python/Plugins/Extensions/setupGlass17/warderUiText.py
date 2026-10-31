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

# On-demand spinner selection status follows the active OSD language.
for _lang, _values in {'sk': ['Načítavam zoznam spinnerov…', 'Online zoznam je nedostupný. Nainštalované spinnery sú k dispozícii.', 'Sťahujem vybraný spinner…', 'Spinner sa nepodarilo stiahnuť. Skúste znova.'], 'cs': ['Načítám seznam spinnerů…', 'Online seznam je nedostupný. Nainstalované spinnery jsou k dispozici.', 'Stahuji vybraný spinner…', 'Spinner se nepodařilo stáhnout. Zkuste znovu.'], 'de': ['Spinner-Liste wird geladen…', 'Online-Liste nicht verfügbar. Installierte Spinner sind verfügbar.', 'Gewählter Spinner wird geladen…', 'Spinner konnte nicht geladen werden. Erneut versuchen.'], 'en': ['Loading spinner list...', 'Online list unavailable. Installed spinners are available.', 'Downloading selected spinner...', 'Spinner download failed. Try again.'], 'pl': ['Wczytywanie listy animacji…', 'Lista online jest niedostępna. Zainstalowane animacje są dostępne.', 'Pobieranie wybranej animacji…', 'Nie udało się pobrać animacji. Spróbuj ponownie.'], 'hu': ['Animációlista betöltése…', 'Az online lista nem érhető el. A telepített animációk elérhetők.', 'A kiválasztott animáció letöltése…', 'Az animáció letöltése sikertelen. Próbálja újra.'], 'ru': ['Загрузка списка анимаций…', 'Онлайн-список недоступен. Установленные анимации доступны.', 'Загрузка выбранной анимации…', 'Не удалось загрузить анимацию. Повторите попытку.'], 'fr': ['Chargement des animations…', 'Liste en ligne indisponible. Les animations installées restent disponibles.', 'Téléchargement de l’animation choisie…', 'Échec du téléchargement. Réessayez.'], 'it': ['Caricamento delle animazioni…', 'Elenco online non disponibile. Le animazioni installate sono disponibili.', 'Download dell’animazione selezionata…', 'Download non riuscito. Riprova.'], 'es': ['Cargando animaciones…', 'Lista en línea no disponible. Las animaciones instaladas están disponibles.', 'Descargando la animación seleccionada…', 'No se pudo descargar. Inténtalo de nuevo.'], 'pt': ['A carregar animações…', 'Lista online indisponível. As animações instaladas estão disponíveis.', 'A transferir a animação selecionada…', 'Não foi possível transferir. Tente novamente.'], 'nl': ['Animatielijst laden…', 'Onlinelijst niet beschikbaar. Geïnstalleerde animaties zijn beschikbaar.', 'Geselecteerde animatie downloaden…', 'Download mislukt. Probeer opnieuw.'], 'ro': ['Se încarcă animațiile…', 'Lista online nu este disponibilă. Animațiile instalate sunt disponibile.', 'Se descarcă animația aleasă…', 'Descărcarea a eșuat. Încercați din nou.'], 'uk': ['Завантаження списку анімацій…', 'Онлайн-список недоступний. Установлені анімації доступні.', 'Завантаження вибраної анімації…', 'Не вдалося завантажити. Спробуйте ще раз.'], 'lt': ['Įkeliamas animacijų sąrašas…', 'Internetinis sąrašas nepasiekiamas. Įdiegtos animacijos pasiekiamos.', 'Atsisiunčiama pasirinkta animacija…', 'Atsisiųsti nepavyko. Bandykite dar kartą.'], 'et': ['Animatsioonide loendi laadimine…', 'Veebiloend pole saadaval. Paigaldatud animatsioonid on saadaval.', 'Valitud animatsiooni allalaadimine…', 'Allalaadimine ebaõnnestus. Proovige uuesti.'], 'al': ['Duke ngarkuar animacionet…', 'Lista në internet nuk është e disponueshme. Animacionet e instaluara janë të disponueshme.', 'Duke shkarkuar animacionin e zgjedhur…', 'Shkarkimi dështoi. Provo sërish.'], 'tr': ['Animasyon listesi yükleniyor…', 'Çevrimiçi liste kullanılamıyor. Yüklü animasyonlar kullanılabilir.', 'Seçilen animasyon indiriliyor…', 'İndirme başarısız. Yeniden deneyin.'], 'fa': ['در حال بارگیری فهرست پویانمایی\u200cها…', 'فهرست آنلاین در دسترس نیست. پویانمایی\u200cهای نصب\u200cشده در دسترس هستند.', 'در حال دریافت پویانمایی انتخاب\u200cشده…', 'دریافت ناموفق بود. دوباره تلاش کنید.'], 'zh': ['正在加载动画列表…', '在线列表不可用。仍可使用已安装的动画。', '正在下载所选动画…', '下载失败，请重试。']}.items():
    TEXT.setdefault(_lang, {}).update(dict(zip(['Loading spinner list...', 'Online list unavailable. Installed spinners are available.', 'Downloading selected spinner...', 'Spinner download failed. Try again.'], _values)))
