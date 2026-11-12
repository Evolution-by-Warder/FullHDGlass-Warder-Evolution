#!/usr/bin/env python3
"""Guard common FullHDGlass movie/EPG column geometry across Enigma2 images.

This checks skin coordinates only; external plugin text rendering and receiver
hardware still need validation on OpenATV 7.6/8.0.1/8.1 and OpenPLi 9.2.
"""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIN = ET.parse(ROOT / "source/package-root/usr/share/enigma2/hd_glass17/skin.xml").getroot()


def widget(screen_name, name):
    screen = SKIN.find("screen[@name='%s']" % screen_name)
    assert screen is not None, screen_name
    found = screen.find("widget[@name='%s']" % name)
    assert found is not None, (screen_name, name)
    return found


def rectangle(element):
    return tuple(map(int, (element.attrib["position"] + "," + element.attrib["size"]).split(",")))


# EMC uses relative positions inside the native MovieCenter list. The EMC
# renderer can shift the text LEFT by bar width + 10 + icon width, and grow
# its text region by exactly the same amount. It must still leave space
# between the progress bar, title, and date even in that worst configuration.
emc = widget("EMCSelection", "list")
assert rectangle(emc) == (700, 120, 1200, 840)
date_pos = int(emc.get("CoolDatePos"))
bar_pos = int(emc.get("CoolBarPos"))
bar_width = int(emc.get("CoolBarSizeSa").split(",")[0])
icon_width = 24  # Native EMC default CoolIconSize, when icons are enabled.
for label_pos_key, label_size_key in (
    ("CoolMoviePos", "CoolMovieSize"),
    ("CoolMoviePiconPos", "CoolMoviePiconSize"),
):
    label_pos = int(emc.get(label_pos_key))
    label_width = int(emc.get(label_size_key))
    first_pixel = label_pos - bar_width - 10 - icon_width
    assert first_pixel >= bar_pos + bar_width + 12, (
        label_pos_key, "title collides with progress/icon area", first_pixel
    )
    assert label_pos + label_width + 12 <= date_pos, (
        label_pos_key, "title collides with date column"
    )
assert date_pos + int(emc.get("CoolDateWidth")) <= rectangle(emc)[2] - 30
assert int(emc.get("CoolFolderSize")) < date_pos

# Native OpenATV EpgList (including the 7.6 EPGSearch plugin) uses
# EpgListSingle=(weekday_width, date_time_width). The EPGSearch plugin adds
# an optional orbital-position column after this pair. Keep the title region
# wide enough for long localized dates and a second orbital column.
params = {p.get("name"): p.get("value") for p in SKIN.findall("./parameters/parameter")}
weekday_width, datetime_width = map(int, params["EpgListSingle"].split(","))
assert 80 <= weekday_width <= 110
assert datetime_width >= 300, "Old narrow datetime field clips localized date/time"
assert datetime_width + weekday_width < 480

search = SKIN.find("screen[@name='EPGSearch']")
assert search is not None, "EPGSearch must have an explicit plugin layout"
sx, sy, sw, sh = rectangle(widget("EPGSearch", "list"))
assert sx >= 840 and sx + sw <= 1890
assert sw - weekday_width - datetime_width - 175 >= 400, (
    "Too little room for titles after date/time plus optional orbital position"
)
description = next(w for w in search.findall("widget")
                   if w.get("source") == "Event")
dx, dy, dw, dh = rectangle(description)
assert dx + dw + 24 <= sx, "Description overlaps search results"
assert sy + sh <= 970 and dy + dh <= 970, "EPG content covers color-key footer"
assert search.find("widget[@source='Service']") is not None
assert search.find("widget[@source='Title']") is not None
for colour in ("red", "green", "yellow", "blue"):
    assert search.find("widget[@source='key_%s']" % colour) is not None

single_width = rectangle(widget("EPGSelection", "list"))[2]
assert single_width - weekday_width - datetime_width >= 430, (
    "Native single EPG title would become too narrow"
)

# Other bundled list/detail screens already separate their text panels in the
# Y-axis. Do not distort these layouts to correct an external plugin's columns.
single = widget("EPGSelection", "list")
assert rectangle(single)[1] + rectangle(single)[3] <= 671
single_cool = widget("CoolSingleGuide", "list")
assert rectangle(single_cool)[1] + rectangle(single_cool)[3] <= 720
search_cool = widget("CoolSearch", "list")
assert rectangle(search_cool)[1] >= 135 + 277

print("PASS: shared EMC columns and native EPG/guide panel boundaries")
