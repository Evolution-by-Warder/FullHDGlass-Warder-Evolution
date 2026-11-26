"""Skin-scoped coloured navigation for the native row-based Multi EPG.

The image owns all EPG data and native list motion. Colours traverse events;
left/right page through channels, and up/down wrap at the list boundaries.
No system input mappings or user EPG settings are rewritten.

Handles OpenATV's EPGSelectionMulti and the legacy EPGSelection controller.
Other EPG views, bouquet selection and other skins retain native actions.
"""

from datetime import date, datetime

DATE_LABELS = {
    "sk": [
        "Dnes",
        "Zajtra",
        "Pondelok",
        "Utorok",
        "Streda",
        "Štvrtok",
        "Piatok",
        "Sobota",
        "Nedeľa"
    ],
    "cs": [
        "Dnes",
        "Zítra",
        "Pondělí",
        "Úterý",
        "Středa",
        "Čtvrtek",
        "Pátek",
        "Sobota",
        "Neděle"
    ],
    "en": [
        "Today",
        "Tomorrow",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ],
    "de": [
        "Heute",
        "Morgen",
        "Montag",
        "Dienstag",
        "Mittwoch",
        "Donnerstag",
        "Freitag",
        "Samstag",
        "Sonntag"
    ],
    "pl": [
        "Dzisiaj",
        "Jutro",
        "Poniedziałek",
        "Wtorek",
        "Środa",
        "Czwartek",
        "Piątek",
        "Sobota",
        "Niedziela"
    ],
    "hu": [
        "Ma",
        "Holnap",
        "Hétfő",
        "Kedd",
        "Szerda",
        "Csütörtök",
        "Péntek",
        "Szombat",
        "Vasárnap"
    ],
    "fr": [
        "Aujourd’hui",
        "Demain",
        "Lundi",
        "Mardi",
        "Mercredi",
        "Jeudi",
        "Vendredi",
        "Samedi",
        "Dimanche"
    ],
    "it": [
        "Oggi",
        "Domani",
        "Lunedì",
        "Martedì",
        "Mercoledì",
        "Giovedì",
        "Venerdì",
        "Sabato",
        "Domenica"
    ],
    "es": [
        "Hoy",
        "Mañana",
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo"
    ],
    "ru": [
        "Сегодня",
        "Завтра",
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ],
    "al": [
        "Sot",
        "Nesër",
        "E hënë",
        "E martë",
        "E mërkurë",
        "E enjte",
        "E premte",
        "E shtunë",
        "E diel"
    ],
    "el": [
        "Σήμερα",
        "Αύριο",
        "Δευτέρα",
        "Τρίτη",
        "Τετάρτη",
        "Πέμπτη",
        "Παρασκευή",
        "Σάββατο",
        "Κυριακή"
    ],
    "et": [
        "Täna",
        "Homme",
        "Esmaspäev",
        "Teisipäev",
        "Kolmapäev",
        "Neljapäev",
        "Reede",
        "Laupäev",
        "Pühapäev"
    ],
    "fa": [
        "امروز",
        "فردا",
        "دوشنبه",
        "سه‌شنبه",
        "چهارشنبه",
        "پنجشنبه",
        "جمعه",
        "شنبه",
        "یکشنبه"
    ],
    "lt": [
        "Šiandien",
        "Rytoj",
        "Pirmadienis",
        "Antradienis",
        "Trečiadienis",
        "Ketvirtadienis",
        "Penktadienis",
        "Šeštadienis",
        "Sekmadienis"
    ],
    "nl": [
        "Vandaag",
        "Morgen",
        "Maandag",
        "Dinsdag",
        "Woensdag",
        "Donderdag",
        "Vrijdag",
        "Zaterdag",
        "Zondag"
    ],
    "pt": [
        "Hoje",
        "Amanhã",
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo"
    ],
    "ro": [
        "Astăzi",
        "Mâine",
        "Luni",
        "Marți",
        "Miercuri",
        "Joi",
        "Vineri",
        "Sâmbătă",
        "Duminică"
    ],
    "tr": [
        "Bugün",
        "Yarın",
        "Pazartesi",
        "Salı",
        "Çarşamba",
        "Perşembe",
        "Cuma",
        "Cumartesi",
        "Pazar"
    ],
    "uk": [
        "Сьогодні",
        "Завтра",
        "Понеділок",
        "Вівторок",
        "Середа",
        "Четвер",
        "П’ятниця",
        "Субота",
        "Неділя"
    ],
    "zh": [
        "今天",
        "明天",
        "星期一",
        "星期二",
        "星期三",
        "星期四",
        "星期五",
        "星期六",
        "星期日"
    ]
}


def event_date(timestamp, language, today=None):
    day = datetime.fromtimestamp(timestamp).date()
    offset = (day - (today or date.today())).days
    names = DATE_LABELS.get(language, DATE_LABELS['en'])
    label = names[offset] if offset in (0, 1) else names[2 + day.weekday()]
    return '%s %d.%02d.' % (label, day.day, day.month)


LABELS = {
    "sk": ("Predchádzajúci", "Nasledujúci"),
    "cs": ("Předchozí", "Následující"),
    "en": ("Previous", "Next"),
    "de": ("Vorherige", "Nächste"),
    "pl": ("Poprzedni", "Następny"),
    "hu": ("Előző", "Következő"),
    "fr": ("Précédent", "Suivant"),
    "it": ("Precedente", "Successivo"),
    "es": ("Anterior", "Siguiente"),
    "al": ("I mëparshmi", "Pasuesi"),
    "el": ("Προηγούμενο", "Επόμενο"),
    "et": ("Eelmine", "Järgmine"),
    "fa": ("قبلی", "بعدی"),
    "lt": ("Ankstesnis", "Kitas"),
    "nl": ("Vorige", "Volgende"),
    "pt": ("Anterior", "Seguinte"),
    "ro": ("Anterior", "Următor"),
    "ru": ("Предыдущая", "Следующая"),
    "tr": ("Önceki", "Sonraki"),
    "uk": ("Попередня", "Наступна"),
    "zh": ("上一节目", "下一节目"),
}
SKIN = "hd_glass17/skin.xml"
SCREEN = "EPGSelectionMulti"


def _language(config):
    """OSD language; never triggers a language or settings change."""
    try:
        value = config.osd.language.value
        if isinstance(value, str):
            code = value.split(".")[0].replace("-", "_").split("_", 1)[0].lower()
            return {"sq": "al", "gr": "el", "cz": "cs", "ua": "uk", "cn": "zh"}.get(code, code)
    except (AttributeError, TypeError, ValueError):
        pass
    return "en"


def install(epg_module, config, info_bar=None):
    """Install once, only when both native coloured action methods exist."""
    multi_type = getattr(epg_module, "EPG_TYPE_MULTI", None)
    if multi_type is None:
        return False

    modern = getattr(epg_module, "EPGSelectionMulti", None)
    if modern is not None and all(callable(getattr(modern, name, None))
                                   for name in ("_btn_yellow", "_btn_blue")):
        controller = modern
        yellow_method, blue_method = "_btn_yellow", "_btn_blue"
        is_modern = True
    else:
        controller = getattr(epg_module, "EPGSelection", None)
        yellow_method, blue_method = "yellowButtonPressed", "blueButtonPressed"
        if controller is None or not all(callable(getattr(controller, name, None))
                                          for name in (yellow_method, blue_method)):
            return False
        is_modern = False

    if controller.__dict__.get("_warderSimpleMultiEpgInstalled", False):
        return True

    yellow_native = getattr(controller, yellow_method)
    blue_native = getattr(controller, blue_method)
    native_init = controller.__init__
    native_selection = getattr(controller, "onSelectionChanged", None)
    native_left = getattr(controller, 'leftPressed', None)
    native_right = getattr(controller, 'rightPressed', None)
    native_up = getattr(controller, 'moveUp', None)
    native_down = getattr(controller, 'moveDown', None)

    def owned(screen):
        try:
            enabled = config.skin.primary_skin.value == SKIN
        except (AttributeError, TypeError, ValueError):
            return False
        if not enabled or getattr(screen, "type", None) != multi_type:
            return False
        name = getattr(screen, "skinName", None)
        if isinstance(name, str):
            return name == SCREEN
        return isinstance(name, (tuple, list)) and SCREEN in name

    def in_epg_list(screen):
        return owned(screen) and not getattr(screen, "bouquetlist_active", False)

    def refresh_labels(screen):
        if not in_epg_list(screen):
            return
        yellow, blue = LABELS.get(_language(config), LABELS["en"])
        for colour, value in (("yellow", yellow), ("blue", blue)):
            try:
                widget = screen["key_" + colour]
            except (KeyError, TypeError, AttributeError):
                continue
            setter = getattr(widget, "setText", None)
            if callable(setter):
                setter(value)

    def refresh_date(screen):
        if not in_epg_list(screen):
            return
        try:
            event = screen["list"].getCurrent()[0]
            text = event_date(event.getBeginTime(), _language(config)) if event is not None else ""
            screen["date"].setText(text)
        except (AttributeError, KeyError, TypeError, ValueError, OverflowError, OSError, RuntimeError):
            pass

    def page(screen, direction, original, *args, **kwargs):
        if in_epg_list(screen):
            mover = getattr(screen, 'prevPage' if direction < 0 else 'nextPage', None)
            if callable(mover):
                result = mover()
                refresh_date(screen)
                return result
        return original(screen, *args, **kwargs)

    def wrap(screen, direction, original, *args, **kwargs):
        if in_epg_list(screen):
            try:
                listing = screen['list']
                index = listing.instance.getCurrentIndex()
                count = len(listing.list)
                if count > 1 and ((direction < 0 and index == 0) or
                                  (direction > 0 and index == count - 1)):
                    listing.instance.moveSelectionTo(count - 1 if direction < 0 else 0)
                    refresh_date(screen)
                    return
            except (AttributeError, KeyError, TypeError, RuntimeError):
                pass
        return original(screen, *args, **kwargs)

    def navigate(screen, direction, fallback, *args, **kwargs):
        if not in_epg_list(screen):
            return fallback(screen, *args, **kwargs)
        if is_modern and getattr(getattr(info_bar, "instance", None),
                                 "LongButtonPressed", False):
            return fallback(screen, *args, **kwargs)
        original = native_left if direction < 0 else native_right
        if callable(original):
            if not callable(getattr(screen, 'leftPressed' if direction < 0 else 'rightPressed', None)):
                return fallback(screen, *args, **kwargs)
            method = lambda: original(screen)
        else:
            # OpenPLi already maps yellow/blue to event movement.
            try:
                update = screen['list'].updateMultiEPG
            except (KeyError, AttributeError, TypeError):
                return fallback(screen, *args, **kwargs)
            method = lambda: update(direction)
        if is_modern:
            close_event = getattr(screen, "closeEventViewDialog", None)
            if callable(close_event):
                close_event()
        method()
        refresh_labels(screen)
        refresh_date(screen)
        return 1  # Consume the colour key; do not run the native action too.

    def yellow(screen, *args, **kwargs):
        return navigate(screen, -1, yellow_native, *args, **kwargs)

    def blue(screen, *args, **kwargs):
        return navigate(screen, +1, blue_native, *args, **kwargs)

    def initialized(screen, *args, **kwargs):
        result = native_init(screen, *args, **kwargs)
        refresh_labels(screen)
        return result

    def selected(screen, *args, **kwargs):
        result = native_selection(screen, *args, **kwargs)
        refresh_labels(screen)
        refresh_date(screen)
        return result

    # All dependencies are validated before mutating class methods.
    setattr(controller, yellow_method, yellow)
    setattr(controller, blue_method, blue)
    controller.__init__ = initialized
    if callable(native_left):
        controller.leftPressed = lambda self, *a, **kw: page(self, -1, native_left, *a, **kw)
    if callable(native_right):
        controller.rightPressed = lambda self, *a, **kw: page(self, 1, native_right, *a, **kw)
    if callable(native_up):
        controller.moveUp = lambda self, *a, **kw: wrap(self, -1, native_up, *a, **kw)
    if callable(native_down):
        controller.moveDown = lambda self, *a, **kw: wrap(self, 1, native_down, *a, **kw)
    if callable(native_selection):
        controller.onSelectionChanged = selected
    controller._warderSimpleMultiEpgInstalled = True
    return True
