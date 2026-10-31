#!/usr/bin/env python3
"""Create a review-only derivative from the unchanged contributed PNG frames.

Preserve the source dish pixels and original brush lettering. Remove the
separate trailing 17, move the remaining caption 15 source pixels to center,
and recolor the foreground to the existing radio-header blue.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/warder/downloads/ui/spinners/bakussa-original.zip'
OUTPUT = ROOT / 'design/spinner-choice/bakussa-blue-centered'
SOURCE_SHA = '47f12b9654349e3bfe909111a5bfdbd260954f311a251b079cf3d1f53848f3ee'
COLOR = '#3CCFFF'


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
    folder = OUTPUT / 'frames'
    folder.mkdir(parents=True, exist_ok=True)
    frames = []
    with zipfile.ZipFile(SOURCE) as archive:
        for index in range(1, 21):
            name = 'wait%d.png' % index
            raw = archive.read('HG glass17 spinner  (bakussa)/' + name)
            # Source dish ends at y=102. Caption starts below it; digits 17
            # are separated from the remaining lettering at source x=99..103.
            caption = subprocess.check_output([
                'convert', 'png:-', '-crop', '100x27+0+103', '+repage', 'png:-'
            ], input=raw)
            caption_file = folder / '.caption.png'
            try:
                caption_file.write_bytes(caption)
                subprocess.run([
                    'convert', 'png:-', '-alpha', 'on', '-channel', 'A',
                    '-region', '130x27+0+103', '-evaluate', 'set', '0',
                    '+region', '+channel', str(caption_file), '-geometry', '+15+103',
                    '-compose', 'over', '-composite', '-channel', 'RGB',
                    '+level-colors', 'black,' + COLOR, '+channel',
                    '-filter', 'Lanczos', '-resize', '104x104',
                    '-define', 'png:color-type=6', '-strip', str(folder / name)
                ], input=raw, check=True)
            finally:
                caption_file.unlink(missing_ok=True)
            encoded = (folder / name).read_bytes()
            frames.append({'name': name, 'sha256': hashlib.sha256(encoded).hexdigest()})
    record = {'schema': 1, 'state': 'visual-review-only', 'author': 'bakussa',
              'source_sha256': SOURCE_SHA, 'color': COLOR, 'size': [104, 104],
              'interval_ms': 100, 'caption': 'FHD Glass', 'digits_17_removed': True,
              'caption_source_crop': [0, 103, 100, 27], 'caption_source_offset': [15, 103],
              'original_archive_unchanged': True, 'published_test_ipk_unchanged': True,
              'frames': frames}
    (OUTPUT / 'review.json').write_text(json.dumps(record, indent=2) + '\n')
    print('Prepared blue, centered-caption derivative for visual review; originals unchanged')


if __name__ == '__main__':
    main()
