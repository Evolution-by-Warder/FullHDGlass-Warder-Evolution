#!/usr/bin/env python3
"""Compile the actual pinned OpenATV allocation predicate, not a lookalike.

This verifies the buffer-allocation decision, not the receiver framebuffer.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


def extract_function(source, name):
    match = re.search(r'static bool ' + re.escape(name) + r'\([^\n]+\)\s*\{', source)
    if not match:
        raise ValueError('Reviewed allocation predicate is missing')
    level = 1
    end = match.end()
    while level:
        level += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[match.start():end]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pixmap', required=True, type=Path)
    parser.add_argument('--header', required=True, type=Path)
    parser.add_argument('--loader', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    args = parser.parse_args()
    source = args.pixmap.read_text()
    threshold = int(re.search(r'#define GFX_SURFACE_ACCELERATION_THRESHOLD (\d+)', source).group(1))
    if threshold != 48000:
        raise ValueError('Review changed OpenATV surface allocation threshold')
    if 'gPixmap(eSize, int bpp, int accel = 0)' not in args.header.read_text():
        raise ValueError('Review changed pixmap constructor allocation default')
    loader = args.loader.read_text()
    if 'directory + "/spinner"' not in loader or '${sysconfdir}/enigma2/spinner' not in loader:
        raise ValueError('This candidate requires the native per-skin spinner loader')
    predicate = extract_function(source, 'is_a_candidate_for_accel')
    harness = '''#include <cassert>
#include <iostream>
#define GFX_SURFACE_ACCELERATION_THRESHOLD %d
struct gUnmanagedSurface { int stride; int bpp; int y; };
%s
int main() {
    gUnmanagedSurface oldBacking{134 * 4, 32, 99};
    gUnmanagedSurface oldIndexed{134, 8, 99};
    gUnmanagedSurface repaired{128 * 4, 32, 88};
    assert(is_a_candidate_for_accel(&oldBacking));
    assert(!is_a_candidate_for_accel(&oldIndexed));
    assert(!is_a_candidate_for_accel(&repaired));
    assert(repaired.y * repaired.stride == 45056);
    std::cout << "PASS: actual OpenATV predicate: old backing GPU candidate; new frames/backing CPU";
}
''' % (threshold, predicate)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / 'allocation.cpp').write_text(harness)
        subprocess.run(['g++', '-std=c++17', '-Wall', '-Wextra', '-Werror', str(root / 'allocation.cpp'), '-o', str(root / 'allocation')], check=True)
        result = subprocess.check_output([str(root / 'allocation')], text=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps({'scope': 'Compiled original upstream allocation predicate',
        'threshold': threshold, 'old_backing_bytes': 53064, 'new_frame_and_backing_bytes': 45056,
        'old_backing_acceleration_candidate': True, 'new_frame_and_backing_acceleration_candidate': False,
        'source_sha256': hashlib.sha256(args.pixmap.read_bytes()).hexdigest(),
        'receiver_test': False}, indent=2) + '\n')
    print(result)


if __name__ == '__main__':
    main()
