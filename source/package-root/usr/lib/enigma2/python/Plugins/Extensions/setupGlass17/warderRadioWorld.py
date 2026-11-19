"""Install signed Radio Browser world bouquet archives onto external PATHS.

This module never runs HTTP, imports Enigma GUI, or touches TV/SAT picons.
Run install_world() in a background worker. Only the selected country is
activated locally, without any Radio Browser request.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile
from zipfile import ZipFile, BadZipFile

from . import warderRadioPackages as country_package

COUNTRY = re.compile(r'^[A-Z]{2}$')
SHA = re.compile(r'^[0-9a-f]{64}$')
WORLD_NAME = 'radio-world'
OWNER = '.warder-world-owned.json'
MAX_ARCHIVE = 256 * 1024 * 1024
MAX_UNPACKED = 512 * 1024 * 1024
MAX_INDEX = 1024 * 1024
MAX_OWNER = 4 * 1024 * 1024
MAX_MEMBER = 24 * 1024 * 1024
MAX_COUNTRIES = 250


def _digest(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(256 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def _safe_directory(root):
    root = Path(root)
    if (root.name != 'hdg17_files' or root.is_symlink() or
            not root.is_dir()):
        return False
    return True


def _json_file(path, maximum):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > maximum:
        raise ValueError('Missing or unsafe world ownership file')
    try:
        result = json.loads(path.read_text(encoding='utf-8'))
    except (UnicodeError, ValueError):
        raise ValueError('Invalid world ownership JSON')
    if not isinstance(result, dict):
        raise ValueError('Invalid world ownership object')
    return result


def _owner_ok(folder):
    """Protect user modifications before an existing radio-world is replaced."""
    if folder.is_symlink():
        return False
    if not folder.exists():
        return True
    if not folder.is_dir():
        return False
    try:
        metadata = _json_file(folder/OWNER, MAX_OWNER)
        if metadata.get('owner') != 'WarderRadioLive' or not SHA.fullmatch(
                str(metadata.get('archive_sha256', ''))):
            return False
        files = metadata.get('files')
        if not isinstance(files, dict) or len(files) > 751:
            return False
        allowed = set(files)
        actual = set()
        for child in folder.rglob('*'):
            if child.is_symlink():
                return False
            if child.is_file():
                actual.add(child.relative_to(folder).as_posix())
            elif not child.is_dir():
                return False
        if actual != allowed | {OWNER}:
            return False
        for name, sha in files.items():
            if (not isinstance(name, str) or
                    not re.fullmatch(r'(?:bouquets/[A-Z]{2}\.radio|catalog/[A-Z]{2}\.json|manifests/[A-Z]{2}\.json|index\.json)', name)
                    or not isinstance(sha, str) or not SHA.fullmatch(sha)):
                return False
            file = folder/name
            if not file.is_file() or file.is_symlink() or _digest(file) != sha:
                return False
        return True
    except (OSError, ValueError):
        return False


def _verify_index(index):
    if (not isinstance(index, dict) or index.get('schema') != 1 or
            index.get('source') != 'WarderRadio.RadioBrowser' or
            not isinstance(index.get('countries'), dict)):
        raise ValueError('Unexpected Radio Browser snapshot index')
    codes = index['countries']
    if (not 1 <= len(codes) <= MAX_COUNTRIES or
            type(index.get('country_count')) is not int or
            index['country_count'] != len(codes) or
            type(index.get('station_count')) is not int):
        raise ValueError('Incomplete world country index')
    if any(not COUNTRY.fullmatch(code) for code in codes):
        raise ValueError('Unknown world country code')
    total = 0
    for code, entry in codes.items():
        if (not isinstance(entry, dict) or
                type(entry.get('stations')) is not int or
                not 0 < entry['stations'] <= 12000 or
                not isinstance(entry.get('bouquet_sha256'), str) or
                not SHA.fullmatch(entry['bouquet_sha256']) or
                not isinstance(entry.get('catalog_sha256'), str) or
                not SHA.fullmatch(entry['catalog_sha256'])):
            raise ValueError('Invalid index country identity')
        total += entry['stations']
    if total != index['station_count']:
        raise ValueError('World station count mismatch')
    return codes


def _manifest_match(code, index_entry, manifest):
    if (manifest.get('country') != code or
            manifest.get('catalogue_complete') is not True or
            manifest.get('stations') != index_entry['stations'] or
            manifest.get('name') != index_entry.get('name')):
        raise ValueError('World country manifest mismatch')
    files = manifest.get('files')
    if not isinstance(files, dict):
        raise ValueError('World country manifest is missing files')
    for kind, key in [('bouquets','bouquet_sha256'),('catalog','catalog_sha256')]:
        suffix='radio' if kind=='bouquets' else 'json'
        entry=files.get(f'{kind}/{code}.{suffix}')
        if not isinstance(entry, dict) or entry.get('sha256') != index_entry[key]:
            raise ValueError('World country checksum inventory mismatch')


def install_world(archive, sha256, paths_root, require_external=True,
                  expected_countries=None):
    """Stage, fully verify and atomically swap the world snapshot directory.

    The caller obtains the expected digest from the trusted GitHub release
    index, not from the ZIP being installed. Does not modify /etc/enigma2.
    """
    root=Path(paths_root)
    if not _safe_directory(root) or (
            require_external and root.stat().st_dev == Path('/').stat().st_dev):
        return {'changed':False,'skipped':'unsafe-storage'}
    archive=Path(archive)
    if (not isinstance(sha256,str) or not SHA.fullmatch(sha256) or
            archive.is_symlink() or not archive.is_file() or
            not 0 < archive.stat().st_size <= MAX_ARCHIVE):
        raise ValueError('Invalid world ZIP or expected checksum')
    if _digest(archive) != sha256:
        raise ValueError('World ZIP SHA-256 mismatch')
    target=root/WORLD_NAME
    if not _owner_ok(target):
        return {'changed':False,'skipped':'unowned-world-folder'}
    if target.exists():
        state=_json_file(target/OWNER, MAX_OWNER)
        if state.get('archive_sha256') == sha256:
            return {'changed':False,'skipped':'already-current',
                    'countries':state.get('countries',0)}
    stage=Path(tempfile.mkdtemp(prefix='.warder-world-stage-',dir=str(root)))
    previous=None
    try:
        with ZipFile(archive) as z:
            infos=z.infolist()
            if len(infos)>1+3*MAX_COUNTRIES or len(infos) != len(set(i.filename for i in infos)):
                raise ValueError('Duplicate or oversized world archive inventory')
            filenames={i.filename for i in infos}
            indexfile='index.json'
            if indexfile not in filenames:
                raise ValueError('Missing world index')
            indexinfo=z.getinfo(indexfile)
            if indexinfo.file_size>MAX_INDEX:
                raise ValueError('Oversized world index')
            index=json.loads(z.read(indexfile).decode('utf-8'))
            codes=_verify_index(index)
            if (expected_countries is not None and
                    (type(expected_countries) is not int or
                     len(codes) != expected_countries)):
                raise ValueError('Published country index count mismatch')
            allowed={indexfile}
            for code in codes:
                allowed.update((f'bouquets/{code}.radio',f'catalog/{code}.json',
                                f'manifests/{code}.json'))
            if filenames != allowed:
                raise ValueError('Incomplete or foreign world archive members')
            total=0
            saved={}
            for info in infos:
                relative=info.filename
                if (info.is_dir() or stat.S_ISLNK(info.external_attr >> 16) or
                        info.file_size > (MAX_INDEX if relative==indexfile else MAX_MEMBER)):
                    raise ValueError('Unsafe world ZIP member')
                total+=info.file_size
                if total>MAX_UNPACKED:
                    raise ValueError('World ZIP decompression size limit')
                path=stage/relative
                path.parent.mkdir(parents=True,exist_ok=True)
                digest=hashlib.sha256()
                count=0
                with z.open(info) as handle, path.open('xb') as output:
                    for block in iter(lambda:handle.read(256*1024),b''):
                        count+=len(block)
                        if count>info.file_size:
                            raise ValueError('Unexpected inflated world member')
                        output.write(block)
                        digest.update(block)
                if count!=info.file_size:
                    raise ValueError('Truncated world ZIP member')
                saved[relative]=digest.hexdigest()
        for code, identity in codes.items():
            _,_,manifest=country_package.verified_country(stage, code)
            _manifest_match(code,identity,manifest)
        (stage/OWNER).write_text(json.dumps({
            'owner':'WarderRadioLive','archive_sha256':sha256,
            'countries':len(codes),'files':saved},sort_keys=True),
            encoding='utf-8')
        if target.exists():
            previous=Path(tempfile.mkdtemp(prefix='.warder-world-old-',dir=str(root)))
            previous.rmdir()
            os.replace(str(target),str(previous))
        try:
            os.replace(str(stage),str(target))
        except OSError:
            if previous is not None and previous.exists() and not target.exists():
                os.replace(str(previous),str(target))
                previous=None
            raise
        if previous is not None:
            shutil.rmtree(previous)
            previous=None
        return {'changed':True,'countries':len(codes),
                'stations':index['station_count'],'sha256':sha256}
    except BadZipFile:
        raise ValueError('Invalid world archive')
    finally:
        if stage.exists():
            shutil.rmtree(stage)




def cached_country(paths_root, code):
    """Cheap read-only GUI hint; activation subprocess does full SHA verification.

    Do not count every PNG or parse the entire station catalogue on Enigma's
    event loop. This is a hint only, never a trust/ownership authorization.
    """
    if not isinstance(code, str) or not COUNTRY.fullmatch(code):
        return None
    root = Path(paths_root)
    folder = root / WORLD_NAME
    try:
        if not _safe_directory(root) or folder.is_symlink() or not folder.is_dir():
            return None
        owner = _json_file(folder / OWNER, MAX_OWNER)
        if owner.get('owner') != 'WarderRadioLive':
            return None
        digest = owner.get('archive_sha256')
        if not isinstance(digest, str) or not SHA.fullmatch(digest):
            return None
        index = _json_file(folder / 'index.json', MAX_INDEX)
        countries = _verify_index(index)
        if code not in countries:
            return None
        for dirname, ext in (('bouquets', 'radio'), ('catalog', 'json'),
                             ('manifests', 'json')):
            item = folder / dirname / (code + '.' + ext)
            if item.is_symlink() or not item.is_file():
                return None
        return digest
    except (OSError, ValueError, TypeError):
        return None


def activate_from_world(paths_root, code, enigma_directory):
    """Fast offline country selection; never validates or scans other countries."""
    root=Path(paths_root)
    current=root/WORLD_NAME
    if not _safe_directory(root) or current.is_symlink() or not current.is_dir():
        return {'changed':False,'skipped':'missing-world-snapshot'}
    owner=_json_file(current/OWNER,MAX_OWNER)
    if owner.get('owner')!='WarderRadioLive':
        return {'changed':False,'skipped':'unowned-world-snapshot'}
    return country_package.activate_local(current,code,enigma_directory)
