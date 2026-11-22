# -*- coding: utf-8 -*-
"""Read native RDS/RT+ metadata for DVB radio without network or GUI changes.

OpenATV RdsInfo uses service.rdsDecoder().getText(iRdsDecoder.RadioText /
RtpText). The native RT+ decoder emits "title (artist)" only for verified
RT+ content types 1 (item.title) and 4 (item.artist). Ordinary RadioText is
unstructured station prose and must never be fabricated into song identity.
"""
import re


def _clean(value):
    if not isinstance(value, str):
        return ""
    return " ".join(re.sub(r"[\x00-\x1f\x7f\x86\x87]", " ", value).split())[:512]


def parse_rtplus(text):
    """Return only the native RT+ title/artist combination, never a guess."""
    value = _clean(text)
    if not value:
        return "", ""
    # Native eDVBRdsDecoder::processData formats 1:title 4:artist
    # as '%s (%.60s)'; a title without an artist is just a title.
    match = re.fullmatch(r"(.+?)\s+\(([^()]+)\)", value)
    if match:
        title, artist = match.group(1).strip(), match.group(2).strip()
        if title and artist:
            return artist, title
    return "", value


def native_rds(service):
    """Return (artist, title, raw_text, raw_caption).

    A real RT+ pair populates artist/title. A lone RT+ title populates
    title only. Plain RadioText remains raw with a truthful caption,
    because Enigma2 doesn't expose artist/song fields for its prose.
    """
    try:
        decoder = service.rdsDecoder() if service is not None else None
        if not decoder:
            return "", "", "", ""
        from enigma import iRdsDecoder
    except (AttributeError, ImportError, RuntimeError):
        return "", "", "", ""

    def read(name):
        try:
            kind = getattr(iRdsDecoder, name, None)
            return _clean(decoder.getText(kind)) if kind is not None else ""
        except (AttributeError, TypeError, RuntimeError, ValueError):
            return ""

    rtp = read("RtpText")
    if rtp:
        artist, title = parse_rtplus(rtp)
        return artist, title, "", ""
    radio_text = read("RadioText")
    return "", "", radio_text, ("RDS TEXT" if radio_text else "")
