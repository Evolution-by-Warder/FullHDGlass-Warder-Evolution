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
    pairs = ((ORIGINAL_CONFIG.encode(), REVISED_CONFIG.encode()),
             (ORIGINAL_HELP.encode(), REVISED_HELP.encode()))
    # Before #151 main had the original 80px help; after the verified
    # merge it already has the reviewed 120px help. Accept only those two
    # complete known baselines, never a partial or arbitrary geometry edit.
    original_mode = all(original.count(before) == 1 and original.count(after) == 0
                        for before, after in pairs)
    reviewed_mode = all(original.count(after) == 1 and original.count(before) == 0
                        for before, after in pairs)
    if not (original_mode or reviewed_mode):
        raise AssertionError('Approved main Setup geometry drift; manual review required')
    if reviewed_mode:
        return data  # Current main already contains the approved change.
    revised = original
    for before, after in pairs:
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
