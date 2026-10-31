#!/usr/bin/env python3
"""Transcode the owner's original animation for the native PNG spinner.

Retain frame order and artwork, use a fixed aspect-fit/premultiplied resample,
and keep every decoded frame and backing surface below the reviewed OpenATV
hardware-allocation threshold. No receiver-time drawing or file replacement.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'design/spinner-repair'
SIZE = (128, 88)
INNER = (120, 84)
THRESHOLD = 48000


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def build(output):
    original = json.loads((DESIGN / 'source.json').read_text())
    output.mkdir(parents=True, exist_ok=True)
    result = []
    rectangle = None
    for entry in original['frames']:
        raw = (DESIGN / 'original' / entry['name']).read_bytes()
        if sha(raw) != entry['sha256']:
            raise ValueError('Original frame changed: ' + entry['name'])
        with Image.open(io.BytesIO(raw)) as image:
            if image.size != (134, 99):
                raise ValueError('Unexpected original canvas')
            # Premultiplication avoids dark fringes during alpha resampling.
            fitted = ImageOps.contain(image.convert('RGBA').convert('RGBa'), INNER,
                                     method=Image.Resampling.LANCZOS).convert('RGBA')
        offset = ((SIZE[0] - fitted.width) // 2, (SIZE[1] - fitted.height) // 2)
        geometry = {'size': list(fitted.size), 'offset': list(offset)}
        if rectangle is not None and rectangle != geometry:
            raise ValueError('Frames must share one fixed transform')
        rectangle = geometry
        frame = Image.new('RGBA', SIZE, (0, 0, 0, 0))
        frame.paste(fitted, offset)  # Copy RGBA exactly, without applying alpha twice.
        packed = io.BytesIO()
        frame.save(packed, format='PNG', compress_level=9)
        encoded = packed.getvalue()
        if encoded[25] != 6 or struct.unpack('>II', encoded[16:24]) != SIZE:
            raise ValueError('Expected truecolor RGBA PNG')
        (output / entry['name']).write_bytes(encoded)
        result.append({'name': entry['name'], 'sha256': sha(encoded),
                       'rgba_sha256': sha(frame.tobytes()), 'bytes': len(encoded)})
    record = {'schema': 1, 'source_package_sha256': original['source_package_sha256'],
              'frame_count': len(result), 'size': list(SIZE), 'png_color_type': 6,
              'decoded_stride': SIZE[0] * 4, 'decoded_surface_bytes': SIZE[0] * SIZE[1] * 4,
              'reviewed_stock_accel_threshold': THRESHOLD,
              'original_backing_surface_bytes': 134 * 99 * 4,
              'fixed_transform': rectangle, 'interval_ms': 100,
              'original_artwork_retained': True, 'receiver_validated': False,
              'frames': result}
    if record['decoded_surface_bytes'] >= THRESHOLD:
        raise ValueError('Spinner would enter the reviewed automatic acceleration path')
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DESIGN / 'frames')
    args = parser.parse_args()
    record = build(args.output)
    (DESIGN / 'candidate.json').write_text(json.dumps(record, indent=2) + '\n')
    print('Built %d RGBA frames, %dx%d; %d bytes per decoded surface < %d' % (
        record['frame_count'], *SIZE, record['decoded_surface_bytes'], THRESHOLD))


if __name__ == '__main__':
    main()
