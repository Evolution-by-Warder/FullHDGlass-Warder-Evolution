#!/usr/bin/env python3
"""Patch Enigma2's native bar event lookup without fake progressbars or masks.

A null celServiceInfo font prevents the text branch from populating evt. The
native progressbar later tests evt and disappears. Fetch evt independently in
that branch. Apply to native Enigma2 *source* as part of an image build.
"""
from pathlib import Path
import re
import sys


def patch(source: str) -> str:
    # OpenATV versions differ in the trailing progressbar condition
    # (notably two-line modes). Preserve it exactly; touch only event lookup.
    pattern = re.compile(
        r"(?m)^(?P<indent>[ \\t]*)eRect area = m_element_position\\[celServiceEventProgressbar\\];\\n"
        r"(?P=indent)if \\(area\\.width\\(\\) > 0 && evt && [^\\n]+"
    )
    matches = list(pattern.finditer(source))
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one native progressbar paint anchor; found %d" % len(matches))
    match = matches[0]
    indent = match.group("indent")
    insert = (
        indent + "// Fetch progress events even when the native EPG text font is disabled.\\n"
        + indent + "if (area.width() > 0 && !evt && isPlayable && service_info)\\n"
        + indent + "\\tservice_info->getEvent(*m_cursor, evt);\\n"
    )
    original = match.group(0)
    first_line = original.split("\\n", 1)[0]
    return source[:match.start()] + first_line + "\\n" + insert + original.split("\\n", 1)[1] + source[match.end():]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply-native-progressbar-event-fix.py /path/to/lib/service/listboxservice.cpp")
    path = Path(sys.argv[1])
    old = path.read_text(encoding="utf-8")
    updated = patch(old)
    path.write_text(updated, encoding="utf-8")
    print("Native progressbar event lookup patched:", path)
