"""Display the original help illustrations over the settings panel background.

Only byte-identical illustrations from the approved help bundle are themed.
Precomputed masks identify the background for navy tinting; no pixel is removed.
The original files are never changed. No Pillow or extra receiver dependency.
"""
import base64
import hashlib
import json
import os
import struct
import tempfile
import zlib

_INDEX = None
_STYLE = 'navy-opaque-v2'
_BACKGROUND = (16, 33, 54)
_SIGNATURE = b'\x89PNG\r\n\x1a\n'


def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else b if pb <= pc else c


def decode_png(raw):
    """Decode the bundle's non-interlaced 8-bit palette/RGB/RGBA PNGs."""
    if raw[:8] != _SIGNATURE:
        raise ValueError('Not a PNG')
    offset = 8
    image_data = []
    palette = None
    transparency = b''
    width = height = kind = channels = None
    while offset + 12 <= len(raw):
        length = struct.unpack('>I', raw[offset:offset + 4])[0]
        tag = raw[offset + 4:offset + 8]
        data = raw[offset + 8:offset + 8 + length]
        if len(data) != length:
            raise ValueError('Truncated PNG')
        if tag == b'IHDR':
            width, height, bits, kind, compression, filtering, interlace = struct.unpack('>IIBBBBB', data)
            if bits != 8 or kind not in (2, 3, 6) or compression or filtering or interlace:
                raise ValueError('Unsupported PNG format')
            if width != 882 or height != 300:
                raise ValueError('Unexpected help dimensions')
            channels = {2: 3, 3: 1, 6: 4}[kind]
        elif tag == b'PLTE':
            palette = data
        elif tag == b'tRNS':
            transparency = data
        elif tag == b'IDAT':
            image_data.append(data)
        elif tag == b'IEND':
            break
        offset += length + 12
    if channels is None:
        raise ValueError('Missing PNG header')
    stride = width * channels
    expected = height * (stride + 1)
    unpacker = zlib.decompressobj()
    packed = unpacker.decompress(b''.join(image_data), expected + 1)
    if len(packed) != expected or not unpacker.eof:
        raise ValueError('Invalid PNG data length')
    rows = bytearray(height * stride)
    previous = bytearray(stride)
    for y in range(height):
        start = y * (stride + 1)
        algorithm = packed[start]
        row = bytearray(packed[start + 1:start + stride + 1])
        if algorithm == 1:
            for x in range(channels, stride):
                row[x] = (row[x] + row[x - channels]) & 255
        elif algorithm == 2:
            for x in range(stride):
                row[x] = (row[x] + previous[x]) & 255
        elif algorithm in (3, 4):
            for x in range(stride):
                left = row[x - channels] if x >= channels else 0
                upper_left = previous[x - channels] if x >= channels else 0
                predictor = (left + previous[x]) // 2 if algorithm == 3 else _paeth(left, previous[x], upper_left)
                row[x] = (row[x] + predictor) & 255
        elif algorithm != 0:
            raise ValueError('Unknown PNG filter')
        rows[y * stride:(y + 1) * stride] = row
        previous = row
    if kind == 6:
        return width, height, rows
    result = bytearray(width * height * 4)
    if kind == 3:
        if palette is None:
            raise ValueError('Missing palette')
        colors = [palette[i:i + 3] + bytes([transparency[i // 3] if i // 3 < len(transparency) else 255])
                  for i in range(0, len(palette), 3)]
        for i, index in enumerate(rows):
            result[i * 4:i * 4 + 4] = colors[index]
    else:
        for i in range(width * height):
            result[i * 4:i * 4 + 4] = rows[i * 3:i * 3 + 3] + b'\xff'
    return width, height, result


def encode_png(width, height, rgba):
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    stride = width * 4
    rows = b''.join(b'\x00' + rgba[y * stride:(y + 1) * stride] for y in range(height))
    return (_SIGNATURE + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows, 6)) + chunk(b'IEND', b''))


def _index():
    global _INDEX
    if _INDEX is None:
        with open(os.path.join(os.path.dirname(__file__), 'warder-help-masks.json'), 'r') as stream:
            _INDEX = json.load(stream)
    return _INDEX


def render(raw, entry):
    width, height, rgba = decode_png(raw)
    count = width * height
    encoded = base64.b64decode(entry['mask'])
    mask = zlib.decompress(encoded)
    if len(mask) != (count + 7) // 8:
        raise ValueError('Invalid help mask')
    for i in range(count):
        if not (mask[i >> 3] & (128 >> (i & 7))):
            # Preserve the original alpha and luminance/shape of the complete
            # illustration. Tint background pixels instead of erasing them.
            for channel, offset in enumerate(_BACKGROUND):
                rgba[i * 4 + channel] = min(255, rgba[i * 4 + channel] + offset)
    return encode_png(width, height, rgba)


def themed_path(filename, cache_dir=None):
    """Return a cached opaque navy variant, or the unchanged source on error."""
    temporary = None
    try:
        with open(filename, 'rb') as stream:
            raw = stream.read(4 * 1024 * 1024 + 1)
        if len(raw) > 4 * 1024 * 1024:
            return filename
        digest = hashlib.sha256(raw).hexdigest()
        entry = _index()['images'].get(digest)
        if entry is None:
            return filename
        cache = cache_dir or '/tmp/warder-help-art-v2'
        os.makedirs(cache, mode=0o700, exist_ok=True)
        revision = hashlib.sha256((_STYLE + ':' + entry['mask']).encode('ascii')).hexdigest()[:12]
        target = os.path.join(cache, digest + '-' + revision + '.png')
        if os.path.isfile(target):
            return target
        result = render(raw, entry)
        with tempfile.NamedTemporaryFile(dir=cache, prefix='.help-', delete=False) as stream:
            temporary = stream.name
            stream.write(result)
        os.replace(temporary, target)
        temporary = None
        return target
    except Exception:
        return filename
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except OSError:
                pass
