# -*- coding: utf-8 -*-
"""Warder Radio OLED screensaver geometry, shared across DVB, DAB and streams.

Independent of Enigma2 so it can be checked offline. Layout follows the
compact moving panel arrangement of Radio-Warder-Evolution/screensaver.py.
"""
from xml.sax.saxutils import escape

DELAYS = (0, 10, 20, 30, 60)
PANELS = (
    ("clockbox", (488, 748, 835, 68)),
    ("playingbox", (488, 236, 330, 48)),
    ("stationbox", (488, 304, 835, 109)),
    ("artbox", (488, 438, 280, 280)),
    ("songbox", (788, 438, 535, 179)),
    ("spectrum", (788, 640, 535, 79)),
)
PICTURES = ("saver_picon", "saver_cover")
CYAN = "#0014d9ed"
PANEL = "#0007131b"
TEXT = "#e7f5fb"


def delay_seconds(value):
    try:
        number = int(value)
    except (ValueError, TypeError):
        return 0
    return number if number in DELAYS else 0


def bounded_motion(offset, direction, step=(7, 5), limit=(90, 60)):
    output, directions = [], []
    for current, velocity, stride, bound in zip(offset, direction, step, limit):
        next_position = current + velocity * stride
        if next_position >= bound:
            next_position, velocity = bound, -1
        elif next_position <= -bound:
            next_position, velocity = -bound, 1
        output.append(next_position)
        directions.append(velocity)
    return tuple(output), tuple(directions)


def make_widgets():
    """Native Enigma2 widgets and original FHD positions; reference scaling is automatic."""
    positions, markup = {}, []

    def widget(name, rect, font=24, bg=None, color=TEXT,
               z=84, align="left", pixmap=False):
        x, y, w, h = rect
        positions[name] = rect
        if pixmap:
            attributes = ' alphatest="blend" scale="1"'
        else:
            attributes = (' font="Regular;%d" foregroundColor="%s"'
                          ' backgroundColor="%s" halign="%s" valign="center"'
                          ' noWrap="1" transparent="%d"' %
                          (font, color, bg or "#ff000000", align, 0 if bg else 1))
        markup.append('<widget name="%s" position="%s,%s" size="%s,%s"'
                      ' zPosition="%d"%s />' % (escape(name), x, y, w, h, z, attributes))

    widget("saver_black", (0, 0, 1920, 1080), bg="#000000", z=80)
    for label, (x, y, w, h) in PANELS:
        prefix = "saver_" + label
        widget(prefix + "_fill", (x, y, w, h), bg=PANEL, z=81)
        for side, rect in (("top", (x, y, w, 2)),
                           ("bottom", (x, y + h - 2, w, 2)),
                           ("left", (x, y, 2, h)),
                           ("right", (x + w - 2, y, 2, h))):
            widget(prefix + "_" + side, rect, bg=CYAN, z=82)

    widget("saver_date", (505, 759, 440, 46), font=19, z=83)
    widget("saver_time", (955, 757, 190, 48), font=30, z=83)
    widget("saver_head", (517, 243, 290, 32), font=22,
           color="#49e7ff", z=83)
    widget("saver_picon", (511, 316, 128, 84), pixmap=True)
    widget("saver_station", (659, 320, 640, 44), font=29, z=83)
    widget("saver_group", (659, 368, 640, 34), font=21,
           color="#9fd3e8", z=83)
    widget("saver_cover", (498, 448, 260, 260), pixmap=True)
    widget("saver_artist_caption", (812, 448, 492, 27),
           font=17, color="#52deef", z=83)
    widget("saver_artist", (812, 477, 492, 50), font=27, z=83)
    widget("saver_track_caption", (812, 537, 492, 27),
           font=17, color="#52deef", z=83)
    widget("saver_track", (812, 562, 492, 44), font=26, z=83)
    widget("saver_signal", (802, 649, 506, 61), font=23,
           color="#52deef", z=83)
    return "".join(markup), positions
