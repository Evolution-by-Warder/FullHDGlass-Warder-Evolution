#!/usr/bin/env python3
"""Lossless build-time PNG compression; preserve dimensions, palette and metadata.

Only replace IDAT, and only when the resulting PNG is smaller. The receiver
performs no compression. No quantization, alpha changes or resampling.
"""
import io
from pathlib import Path
import struct
import zlib
from PIL import Image


def chunks(raw):
    assert raw[:8] == b'\x89PNG\r\n\x1a\n'
    offset = 8
    result = []
    while offset < len(raw):
        length = struct.unpack('>I', raw[offset:offset+4])[0]
        kind = raw[offset+4:offset+8]
        data = raw[offset+8:offset+8+length]
        crc = raw[offset+8+length:offset+12+length]
        assert len(data) == length and crc == struct.pack('>I', zlib.crc32(kind+data) & 0xffffffff)
        result.append((kind, data))
        offset += length + 12
    assert offset == len(raw) and result[-1][0] == b'IEND'
    return result


def encode(parts):
    return b'\x89PNG\r\n\x1a\n' + b''.join(struct.pack('>I', len(data))+kind+data+struct.pack('>I', zlib.crc32(kind+data)&0xffffffff) for kind,data in parts)


def optimize(raw):
    original = chunks(raw)
    if any(kind == b'acTL' for kind,_ in original):
        return raw  # Preserve animated PNGs in their entirety.
    image = Image.open(io.BytesIO(raw))
    output = io.BytesIO()
    image.save(output, format='PNG', optimize=True, compress_level=9)
    candidate = chunks(output.getvalue())
    critical = lambda rows: [(k,v) for k,v in rows if k in (b'IHDR',b'PLTE',b'tRNS')]
    if critical(original) != critical(candidate):
        # Encoder must not change palette, bit depth, transparency or interlace.
        packed = zlib.compress(zlib.decompress(b''.join(d for k,d in original if k==b'IDAT')),9)
    else:
        packed = b''.join(d for k,d in candidate if k==b'IDAT')
    result=[]
    for kind,data in original:
        if kind != b'IDAT':result.append((kind,data))
        elif packed is not None:
            result.append((kind,packed));packed=None
    encoded = encode(result)
    if len(encoded) >= len(raw):return raw
    before = image.convert('RGBA')
    with Image.open(io.BytesIO(encoded)) as after:
        assert after.size == image.size and after.convert('RGBA').tobytes() == before.tobytes()
    assert [(k,d) for k,d in chunks(encoded) if k!=b'IDAT'] == [(k,d) for k,d in original if k!=b'IDAT']
    return encoded


def optimize_tree(root):
    records=[]
    for path in sorted(Path(root).rglob('*.png')):
        raw=path.read_bytes();packed=optimize(raw)
        if packed!=raw:
            path.write_bytes(packed)
            records.append({'path':path.relative_to(root).as_posix(),'before':len(raw),'after':len(packed)})
    return records
