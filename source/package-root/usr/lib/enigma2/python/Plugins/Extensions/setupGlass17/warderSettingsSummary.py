"""Read-only compact diagnostic values for the existing 'Selected settings' line.

The one-line header is useful in support screenshots. Always report the actual
configured ChannelSelection variant and font overrides; do not alter settings.
The EPG flag represents the user's preference, not proof of active scrolling.
"""


# Support-only numbering. Keep the normal menu choice values and Enigma2
# skin template numbers unchanged. 1 is always the factory/default "List".
MENU_DISPLAY_ORDER = (
    "List", "Icons", "Icons Right", "with PIG", "List and Icon",
    "Icons Bar", "simply PIG", "PIG2", "PIG4", "Li2", "Li3",
)


def menu_support_number(value):
    """One-based, stable menu number for screenshots, default List = 1."""
    try:
        return str(MENU_DISPLAY_ORDER.index(str(value)) + 1)
    except ValueError:
        return "?"  # Fail visibly; never call an unknown mode "default".


def channel_diagnostic_suffix(channel_type, epg_scroll_enabled,
                              epg_renderer_allowed, name_font, event_font,
                              row_height, language="en"):
    lang = str(language or "en").replace("-", "_").split("_", 1)[0].lower()
    labels = {
        "sk": ("Výber kanálov", "ZAP", "VYP"),
        "cs": ("Výběr kanálů", "ZAP", "VYP"),
        "en": ("Channel list", "ON", "OFF"),
        "de": ("Kanalliste", "AN", "AUS"),
        "pl": ("Lista kanałów", "WŁ", "WYŁ"),
    }
    channel_label, on, off = labels.get(lang, labels["en"])
    epg_value = on if bool(epg_scroll_enabled) else off
    backend = "GLES" if bool(epg_renderer_allowed) else "NAT"
    fonts = "%s/%s/%s" % (name_font, event_font, row_height)
    return ", %s: %s, EPG: %s/%s, F N/E/R: %s" % (
        channel_label, str(channel_type), epg_value, backend, fonts)
