#!/usr/bin/env python3
"""Allow only the reviewed multiline native Setup help clearance versus main.

This is deliberately an exact whole-file comparison, not an exclusion of Setup:
all other skin lines must remain byte-for-byte identical to the approved main.
"""
import sys
from pathlib import Path

ORIGINAL_CONFIG = '<widget name="config" position="45,60" size="1560,615" font="Prive3;34" itemHeight="45" scrollbarMode="showOnDemand" />'
REVISED_CONFIG = '<widget name="config" position="45,60" size="1560,585" font="Prive3;34" itemHeight="45" scrollbarMode="showOnDemand" />'
ORIGINAL_HELP = '<widget name="description" position="45,690" size="1560,80" font="Prive3;27" halign="center" valign="center" foregroundColor="grey" transparent="1" />'
REVISED_HELP = '<widget name="description" position="45,650" size="1560,120" font="Prive3;25" halign="center" valign="center" foregroundColor="grey" transparent="1" />'


def expected_from_main(data):
    header = b'<screen name="Setup" '
    first = data.find(header)
    if first < 0:
        raise AssertionError('Approved main has no native Setup screen')
    last = data.find(b'</screen>', first)
    if last < 0:
        raise AssertionError('Approved native Setup screen has no end tag')
    original = data[first:last]
    revised = original
    for before, after in ((ORIGINAL_CONFIG, REVISED_CONFIG),
                          (ORIGINAL_HELP, REVISED_HELP)):
        before, after = before.encode(), after.encode()
        if revised.count(before) != 1:
            raise AssertionError('Approved main Setup geometry drift; manual review required')
        revised = revised.replace(before, after, 1)
    return data[:first] + revised + data[last:]


def main():
    if len(sys.argv) != 3:
        raise SystemExit('usage: verify-solo4k-setup-geometry.py approved-main.xml candidate.xml')
    old, new = (Path(path).read_bytes() for path in sys.argv[1:])
    if new != expected_from_main(old):
        raise AssertionError('Unreviewed skin.xml diff: only the exact two Setup widget edits are allowed')
    print('PASS: exact native Setup help-only geometry against approved main; all other skin bytes identical')


if __name__ == '__main__':
    main()
