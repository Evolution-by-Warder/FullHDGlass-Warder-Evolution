"""Compact read-only setup-header diagnostics for receiver support screenshots.

Never changes user configuration. The two EPG flags distinguish the saved
scroll preference from the runtime's permitted GLES renderer: ON/native is a
real diagnostic state, not evidence that scrolling is active.
"""


def channel_diagnostic_suffix(channel_type, scroll_enabled, gles_allowed,
                              service_name_font, service_epg_font, row_height,
                              translate=lambda text: text):
    """Return the extra settings shown after the existing weather icon field.

    Compact enough for the one-line 1920px setup header. Values are direct
    configuration identifiers (including '0' meaning default font size).
    """
    channel = str(channel_type)
    scrolling = "ON" if bool(scroll_enabled) else "OFF"
    renderer = "GLES" if bool(gles_allowed) else "native"
    font_triplet = "%s/%s/%s" % (service_name_font, service_epg_font, row_height)
    return ", %s: %s, EPG rol.: %s/%s, N/E/H: %s" % (
        translate("Channel selection type"), channel,
        scrolling, renderer, font_triplet)
