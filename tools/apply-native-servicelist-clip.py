#!/usr/bin/env python3
"""Bound native OpenATV ServiceListLegacy event text to its own field.

Source-only fix: applies to the Enigma2 C++ checkout for the receiver's
EXACT upstream source revision. It is NOT a skin IPK or an ARM binary.
Do not apply to an unverified running image.
"""
import sys
from pathlib import Path

ANCHOR = "\t\t\t\tpainter.renderPara(para, offset+ePoint(xoffs, yoffs));\n"

PATCH = """\t\t\t\t// Clip only the legacy EPG event label, not the native
\t\t\t\t// progressbar, percentage, remaining time or service name.
\t\t\t\t// Its text paragraph otherwise draws beyond its reserved
\t\t\t\t// field into celServiceEventProgressbar.
\t\t\t\tif (e == celServiceInfo)
\t\t\t\t{
\t\t\t\t\teRect eventClip = m_element_position[celServiceInfo];
\t\t\t\t\tconst eRect progressArea = m_element_position[celServiceEventProgressbar];
\t\t\t\t\t// In right-hand modes, end before the bar/value and gap;
\t\t\t\t\t// for left-hand or disabled modes retain the EPG field.
\t\t\t\t\tif (progressArea.width() > 0 && progressArea.left() > eventClip.left()
\t\t\t\t\t\t&& progressArea.left() < eventClip.right())
\t\t\t\t\t\teventClip.setRight(progressArea.left() - m_items_distances);
\t\t\t\t\tif (eventClip.width() > 0 && eventClip.height() > 0)
\t\t\t\t\t{
\t\t\t\t\t\teventClip.moveBy(offset);
\t\t\t\t\t\tpainter.clip(eventClip);
\t\t\t\t\t\tpainter.renderPara(para, offset+ePoint(xoffs, yoffs));
\t\t\t\t\t\tpainter.clippop();
\t\t\t\t\t}
\t\t\t\t}
\t\t\t\telse
\t\t\t\t\tpainter.renderPara(para, offset+ePoint(xoffs, yoffs));
"""


def patch(source):
    if source.count(ANCHOR) != 1:
        raise RuntimeError("Expected exactly one native renderPara anchor; found %d" % source.count(ANCHOR))
    if "Clip only the legacy EPG event label" in source:
        raise RuntimeError("Patch appears already applied")
    mandatory = ("case celServiceInfo:", "celServiceEventProgressbar",
                 "m_element_position[celServiceInfo].setLeft(",
                 "painter.clip(eRect(offset, m_itemsize))")
    for marker in mandatory:
        if marker not in source:
            raise RuntimeError("Missing OpenATV legacy source contract: " + marker)
    return source.replace(ANCHOR, PATCH, 1)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply-native-servicelist-clip.py /path/to/lib/service/listboxservice.cpp")
    file = Path(sys.argv[1])
    original = file.read_text(encoding="utf-8")
    updated = patch(original)
    file.write_text(updated, encoding="utf-8")
    print("Applied native ServiceListLegacy EPG-only clipping to", file)


if __name__ == "__main__":
    main()
