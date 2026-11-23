"""Read-only compact diagnostic values for the existing 'Selected settings' line.

The one-line header is useful in support screenshots. Always report the actual
configured ChannelSelection variant and font overrides; do not alter settings.
The EPG flag represents the user's preference, not proof of active scrolling.
"""


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
