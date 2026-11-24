"""Skin-scoped coloured navigation for the native row-based Multi EPG.

The image owns all EPG data, list pagination and input actions. Only yellow
and blue SHORT press are redirected to the same previous/next event methods
already used by LEFT/RIGHT. No keymap or user EPG settings are rewritten.

Handles OpenATV's EPGSelectionMulti and the legacy EPGSelection controller.
Other EPG views, bouquet selection and other skins retain native actions.
"""

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
}
SKIN = "hd_glass17/skin.xml"
SCREEN = "EPGSelectionMulti"


def _language(config):
    """OSD language; never triggers a language or settings change."""
    try:
        value = config.osd.language.value
        if isinstance(value, str):
            return value.replace("-", "_").split("_", 1)[0].lower()
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

    def navigate(screen, direction, fallback, *args, **kwargs):
        if not in_epg_list(screen):
            return fallback(screen, *args, **kwargs)
        if is_modern and getattr(getattr(info_bar, "instance", None),
                                 "LongButtonPressed", False):
            return fallback(screen, *args, **kwargs)
        method = getattr(screen, "leftPressed" if direction < 0 else "rightPressed", None)
        if not callable(method):
            return fallback(screen, *args, **kwargs)
        if is_modern:
            close_event = getattr(screen, "closeEventViewDialog", None)
            if callable(close_event):
                close_event()
        method()
        refresh_labels(screen)
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
        return result

    # All dependencies are validated before mutating class methods.
    setattr(controller, yellow_method, yellow)
    setattr(controller, blue_method, blue)
    controller.__init__ = initialized
    if callable(native_selection):
        controller.onSelectionChanged = selected
    controller._warderSimpleMultiEpgInstalled = True
    return True
