#!/usr/bin/env python3
"""Fix native Enigma2 event lookup for progressbars with EPG text suppressed.

A null celServiceInfo font prevents the text branch from populating evt.
The native bar still needs that event even when EPG text is externally painted.
This edits native C++ source as part of an Enigma2 image build, not the IPK.
"""
from pathlib import Path
import re
import sys


def patch(source: str) -> str:
    # Retain the exact existing native bar condition (two-line variants differ).
    pattern = re.compile(
        r"(?m)^(?P<indent>[ \t]*)eRect area = m_element_position\[celServiceEventProgressbar\];\n"
        r"(?P=indent)if \(area\.width\(\) > 0 && evt && [^\n]+"
    )
    matches = list(pattern.finditer(source))
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one native progressbar paint anchor; found %d" % len(matches))
    match = matches[0]
    indent = match.group("indent")
    original = match.group(0)
    first, rest = original.split("\n", 1)
    added = (
        indent + "// Progress event lookup must not depend on the EPG text font.\n"
        + indent + "if (area.width() > 0 && !evt && isPlayable && service_info)\n"
        + indent + "\tservice_info->getEvent(*m_cursor, evt);\n"
    )
    return source[:match.start()] + first + "\n" + added + rest + source[match.end():]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply-native-progressbar-event-fix.py /path/to/lib/service/listboxservice.cpp")
    path = Path(sys.argv[1])
    original = path.read_text(encoding="utf-8")
    path.write_text(patch(original), encoding="utf-8")
    print("Native progressbar event lookup patched:", path)
