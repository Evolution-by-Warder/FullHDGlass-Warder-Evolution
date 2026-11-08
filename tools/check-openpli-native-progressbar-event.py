#!/usr/bin/env python3
"""Check OpenPLi event retrieval precedes native progress paint.

This does not compile Enigma2; it verifies that the OpenATV-specific native
patch is NOT blindly applied to OpenPLi's structurally different painter.
"""
from pathlib import Path
import sys


def verify(source: str) -> None:
    eager = "bool is_event = isPlayable && service_info && !service_info->getEvent(ref, evt);"
    start = source.find(eager)
    if start < 0:
        raise RuntimeError("OpenPLi eager native event lookup not found")
    event_branch = source.find("if (is_event)", start)
    bar = source.find("eRect progressBarRect = m_element_position[celServiceEventProgressbar];", event_branch)
    if not (start < event_branch < bar):
        raise RuntimeError("OpenPLi native event / progress order changed")
    if source.find("if (is_event)", start, bar) < 0:
        raise RuntimeError("OpenPLi progress branch missing event guard")
    print("OpenPLi native EPG event lookup precedes progress painting: PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: check-openpli-native-progressbar-event.py path/to/listboxservice.cpp")
    verify(Path(sys.argv[1]).read_text(encoding="utf-8"))
