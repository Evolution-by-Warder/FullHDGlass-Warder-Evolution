"""On-demand spinner data. Network is used only by the open selection screen.

No GUI dependencies, persistent logs, scheduled checks or playback workers.
Downloaded frame sets are verified before they become selectable.
"""
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import stat
import struct
import tempfile
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import zipfile
import zlib

BASE = 'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/ui/spinners/online/'
CATALOG_URL = BASE + 'catalog.json'
MAX_CATALOG = 256 * 1024
MAX_ZIP = 1024 * 1024
MAX_THUMB = 48 * 1024


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def resource_url(path, suffix):
    if not isinstance(path, str) or not re.fullmatch(r'(?:archives|thumbnails)/[a-z0-9-]+\.'+suffix, path):
        raise ValueError('Invalid spinner resource path')
    return BASE + path


def fetch(url, maximum, opener=urlopen):
    if not url.startswith(BASE) or urlsplit(url).query or urlsplit(url).fragment:
        raise ValueError('Unexpected spinner source')
    with opener(Request(url, headers={'User-Agent': 'FullHDGlass-spinners/1'}), timeout=12) as response:
        if hasattr(response, 'geturl') and response.geturl() != url:
            raise ValueError('Unexpected spinner redirect')
        raw = response.read(maximum+1)
    if not raw or len(raw) > maximum:
        raise ValueError('Empty or oversized spinner resource')
    return raw


def checked_resource(item, suffix, limit, opener=urlopen):
    if type(item.get('bytes')) is not int or not 0 < item['bytes'] <= limit:
        raise ValueError('Invalid spinner resource size')
    if not re.fullmatch('[0-9a-f]{64}', item.get('sha256', '')):
        raise ValueError('Invalid spinner resource checksum')
    raw = fetch(resource_url(item['path'], suffix), min(item['bytes'], limit), opener)
    if len(raw) != item['bytes'] or digest(raw) != item['sha256']:
        raise ValueError('Spinner resource checksum mismatch')
    return raw


def parse_catalog(raw):
    if len(raw) > MAX_CATALOG:
        raise ValueError('Spinner list is too large')
    data = json.loads(raw)
    if data.get('schema') != 1 or data.get('product') != 'FullHDGlass-spinners':
        raise ValueError('Unsupported spinner list')
    rows, seen = data['entries'], set()
    if not isinstance(rows, list) or not 1 <= len(rows) <= 512:
        raise ValueError('Invalid spinner list length')
    for row in rows:
        key = row['id']
        if not re.fullmatch('[a-z][a-z0-9-]{0,31}', key) or key in seen:
            raise ValueError('Invalid or duplicate spinner identifier')
        seen.add(key)
        for field in ('title', 'author'):
            if not isinstance(row[field], str) or len(row[field]) > 160 or any(ord(c)<32 for c in row[field]):
                raise ValueError('Invalid spinner caption')
        for field, suffix, limit in [('archive', 'zip', MAX_ZIP), ('thumbnail', 'png', MAX_THUMB)]:
            item = row[field]
            resource_url(item['path'], suffix)
            if type(item['bytes']) is not int or not 0 < item['bytes'] <= limit or not re.fullmatch('[0-9a-f]{64}', item['sha256']):
                raise ValueError('Invalid spinner resource')
        if not re.fullmatch('[0-9a-f]{64}', row.get('frames_sha256', '')):
            raise ValueError('Invalid frame list checksum')
    return rows


def frame_digest(frames):
    return digest(json.dumps(frames, sort_keys=True, separators=(',', ':')).encode())


def png(raw, expected_size):
    """Validate bounded, noninterlaced RGBA PNGs without Pillow on the box."""
    if not raw.startswith(b'\x89PNG\r\n\x1a\n') or len(raw) > 128*1024:
        raise ValueError('Invalid spinner PNG')
    pos, compressed, header, ended = 8, bytearray(), False, False
    while pos+12 <= len(raw):
        count = struct.unpack('>I', raw[pos:pos+4])[0]
        tag, body = raw[pos+4:pos+8], raw[pos+8:pos+8+count]
        if len(body) != count or pos+12+count > len(raw):
            raise ValueError('Truncated PNG chunk')
        crc = struct.unpack('>I', raw[pos+8+count:pos+12+count])[0]
        if zlib.crc32(tag+body) & 0xffffffff != crc:
            raise ValueError('PNG checksum mismatch')
        if tag == b'IHDR':
            if header or pos != 8 or count != 13:
                raise ValueError('Invalid PNG header')
            w, h, depth, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', body)
            if (w, h) != tuple(expected_size) or depth != 8 or color != 6 or compression or filtering or interlace:
                raise ValueError('Unexpected spinner PNG format')
            if not (0 < w <= 128 and 0 < h <= 128 and w*h*4 < 48000):
                raise ValueError('Spinner PNG exceeds native bounds')
            header = True
        elif tag == b'IDAT':
            compressed.extend(body)
        elif tag in (b'acTL', b'fcTL', b'fdAT'):
            raise ValueError('Animated preview PNG is not allowed')
        elif tag == b'IEND':
            if count or pos+12 != len(raw):
                raise ValueError('Invalid PNG end')
            ended = True
            break
        pos += count+12
    if not header or not ended or not compressed:
        raise ValueError('Incomplete PNG')
    expected = (w*4+1)*h
    inflater = zlib.decompressobj()
    pixels = inflater.decompress(bytes(compressed), expected+1)
    if len(pixels) != expected or not inflater.eof or inflater.unused_data:
        raise ValueError('Invalid PNG pixels')
    if any(pixels[i] > 4 for i in range(0, expected, w*4+1)):
        raise ValueError('Invalid PNG filter')
    return raw


def archive_data(row, raw, validate_theme):
    if len(raw) != row['archive']['bytes'] or digest(raw) != row['archive']['sha256']:
        raise ValueError('Spinner archive checksum mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = archive.infolist()
        names = [m.filename for m in members]
        if len(names) != len(set(names)) or not 2 <= len(names) <= 68:
            raise ValueError('Invalid spinner ZIP entries')
        if sum(m.file_size for m in members) > 2*1024*1024:
            raise ValueError('Expanded spinner ZIP is too large')
        for member in members:
            mode = member.external_attr >> 16
            if (member.flag_bits & 1 or member.file_size > 128*1024 or
                    stat.S_ISLNK(mode) or member.is_dir() or
                    not re.fullmatch(r'(manifest\.json|AUTOR\.txt|LICENSE\.txt|wait[1-9][0-9]?\.png)', member.filename)):
                raise ValueError('Unsafe spinner ZIP member')
        document = json.loads(archive.read('manifest.json'))
        if document.get('schema') != 1 or document.get('id') != row['id']:
            raise ValueError('Spinner archive identity mismatch')
        theme = document['theme']
        validate_theme(theme)
        if (theme['title'] != row['title'] or theme['author'] != row['author'] or
                frame_digest(theme['frames']) != row['frames_sha256']):
            raise ValueError('Spinner metadata mismatch')
        required = {f['name'] for f in theme['frames']} | {'manifest.json', 'AUTOR.txt'}
        if not required <= set(names) or set(names)-required-{'LICENSE.txt'}:
            raise ValueError('Spinner archive frame list differs')
        frames = {}
        for entry in theme['frames']:
            data = archive.read(entry['name'])
            if digest(data) != entry['sha256']:
                raise ValueError('Spinner frame checksum mismatch')
            frames[entry['name']] = png(data, theme['size'])
    return theme, frames


def local_id(row, backend):
    data = backend.catalog()
    theme = data['themes'].get(row['id'])
    if theme and frame_digest(theme['frames']) == row['frames_sha256']:
        return row['id']
    key = 'dl-' + row['archive']['sha256'][:16]
    return key if key in data['themes'] else None


def install_selected(row, raw, backend, skin_root=None, cache_root=None):
    """Store only a selected, verified set; Save applies it later."""
    theme, frames = archive_data(row, raw, backend.validate_theme)
    root = Path(cache_root if cache_root is not None else backend.DOWNLOAD_ROOT)
    skin = Path(skin_root if skin_root is not None else backend.SKIN_ROOT)
    if root.is_symlink():
        raise ValueError('Linked spinner cache')
    existing = backend.downloaded(root)
    key = 'dl-' + row['archive']['sha256'][:16]
    target = root/key
    if key in existing:
        for name, data in frames.items():
            if (target/name).is_symlink() or (target/name).read_bytes() != data:
                raise ValueError('Stored spinner has changed')
        return key
    if target.exists() or target.is_symlink():
        raise ValueError('Unidentified spinner cache must be preserved')
    active = skin/'spinner'
    if active.is_symlink():
        raise ValueError('Linked active spinner')
    active_hashes = {p.name:digest(p.read_bytes()) for p in active.glob('wait*.png') if p.is_file() and not p.is_symlink()}
    protected = {k for k,v in existing.items() if any(active_hashes.get(f['name']) == f['sha256'] for f in v['theme']['frames'])}
    prune = [k for k in existing if k not in protected]
    if len(existing) >= 2 and not prune:
        raise ValueError('Both stored animations are still in use')
    # Validate every victim completely before creating or deleting anything.
    victims = prune[:max(0, len(existing)-1)]
    for victim in victims:
        folder, record = root/victim, existing[victim]
        if {p.name for p in folder.iterdir()} != {'manifest.json'} | {f['name'] for f in record['theme']['frames']}:
            raise ValueError('User files in spinner cache must be preserved')
        for f in record['theme']['frames']:
            if (folder/f['name']).is_symlink() or digest((folder/f['name']).read_bytes()) != f['sha256']:
                raise ValueError('Modified spinner cache must be preserved')
    root.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.spinner-', dir=str(root)))
    try:
        for name, data in frames.items():
            (stage/name).write_bytes(data)
        record = {'schema':1, 'product':'FullHDGlass-spinner', 'id':key,
                  'remote_id':row['id'], 'archive_sha256':row['archive']['sha256'], 'theme':theme}
        (stage/'manifest.json').write_text(json.dumps(record, ensure_ascii=False))
        stage.chmod(0o755)
        for p in stage.iterdir():
            p.chmod(0o644)
        stage.rename(target)
        for victim in victims:
            folder = root/victim
            for p in folder.iterdir():
                p.unlink()
            folder.rmdir()
        return key
    finally:
        if stage.exists():
            shutil.rmtree(stage)
