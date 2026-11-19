"""Background GitHub snapshot downloader for Warder Radio Live.

The public immutable release provides one world-bouquet ZIP and one original
logo ZIP per country. This module never runs in the GUI event loop, and refuses
unpublished/foreign/index-inconsistent data. Country selection itself stays
offline; only snapshots and selected-country logos use HTTP.

This is a working candidate. The repository's latest.json and production
release are NOT published yet; no automatic scheduler uses this module.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from . import warderRadioWorld as world
from . import warderRadioPackages as packages
from . import warderRadioCountry as country

LATEST_URL = ('https://raw.githubusercontent.com/Evolution-by-Warder/'
              'Radio-Warder-Evolution/main/assets/radio-country/latest.json')
RELEASE_ROOT = ('https://github.com/Evolution-by-Warder/'
                'Radio-Warder-Evolution/releases/download/')
TAG = re.compile(r'^radio-country-20[0-9]{6}$')
ISO = re.compile(r'^[A-Z]{2}$')
SHA = re.compile(r'^[0-9a-f]{64}$')
INDEX_LIMIT = 1024 * 1024
ZIP_LIMIT = world.MAX_ARCHIVE
LOGO_LIMIT = packages.MAX_ZIP


def _trusted_url(value):
    try:
        parsed = urlsplit(value)
        host = parsed.hostname or ''
        return (parsed.scheme == 'https' and parsed.username is None and
                parsed.password is None and parsed.port in (None,443) and
                (host in ('github.com','raw.githubusercontent.com') or
                 host.endswith('.githubusercontent.com')))
    except (TypeError,AttributeError,ValueError):
        return False


def _open(opener, address):
    if not _trusted_url(address):
        raise ValueError('Unexpected country release host')
    response = opener(Request(address, headers={
        'User-Agent':'FullHDGlass-radio-country/1',
        'Accept':'application/octet-stream',
        'Cache-Control':'no-cache'}), timeout=15)
    # github.com releases redirect through GitHub-controlled asset hosts.
    redirected = response.geturl() if callable(getattr(response,'geturl',None)) else address
    if not _trusted_url(redirected):
        response.close()
        raise ValueError('Unexpected country asset redirect')
    return response


def _feed(opener):
    with _open(opener, LATEST_URL) as response:
        content = response.read(INDEX_LIMIT+1)
    if len(content)>INDEX_LIMIT or not content:
        raise ValueError('Invalid radio country index size')
    try:
        data=json.loads(content.decode('utf-8'))
    except (ValueError,UnicodeError):
        raise ValueError('Invalid radio country index')
    if (not isinstance(data,dict) or data.get('schema')!=1 or
            data.get('source')!='WarderRadio.RadioBrowser' or
            not isinstance(data.get('release_tag'),str) or
            not TAG.fullmatch(data['release_tag']) or
            not isinstance(data.get('countries'),dict) or
            not 1<=len(data['countries'])<=250 or
            type(data.get('country_count')) is not int or
            data['country_count']!=len(data['countries'])):
        raise ValueError('Untrusted or incomplete release index')
    blob=data.get('world')
    if (not isinstance(blob,dict) or
            blob.get('file')!='radio-countries-bouquets.zip' or
            not isinstance(blob.get('sha256'),str) or not SHA.fullmatch(blob['sha256']) or
            type(blob.get('bytes')) is not int or not 0<blob['bytes']<=ZIP_LIMIT):
        raise ValueError('Untrusted world release identity')
    for code,record in data['countries'].items():
        if not isinstance(code,str) or not ISO.fullmatch(code) or not isinstance(record,dict):
            raise ValueError('Untrusted country index')
        logos=record.get('logos')
        if (not isinstance(logos,dict) or
                logos.get('file')!=code+'.zip' or
                type(logos.get('bytes')) is not int or
                not 0<logos['bytes']<=LOGO_LIMIT or
                not isinstance(logos.get('sha256'),str) or
                not SHA.fullmatch(logos['sha256']) or
                type(record.get('logo_package_complete')) is not bool):
            raise ValueError('Untrusted country logo listing')
    return data


def _asset(index, name):
    if name not in ('radio-countries-bouquets.zip',) and not (
            re.fullmatch(r'[A-Z]{2}\.zip',name)):
        raise ValueError('Unsafe release asset name')
    return RELEASE_ROOT+index['release_tag']+'/'+name


def _download(opener, url, parent, expected_hash, expected_size, limit):
    """Write a verified ZIP in the external staging directory, not RAM/flash."""
    parent=Path(parent)
    if parent.is_symlink() or not parent.is_dir():
        raise ValueError('Unsafe radio cache staging location')
    if (not SHA.fullmatch(expected_hash) or
            type(expected_size) is not int or
            not 0<expected_size<=limit):
        raise ValueError('Invalid expected asset digest')
    fd, filename=tempfile.mkstemp(prefix='.warder-download-',dir=str(parent))
    temp=Path(filename)
    digest=hashlib.sha256()
    total=0
    try:
        with os.fdopen(fd,'wb') as file, _open(opener,url) as response:
            while True:
                chunk=response.read(256*1024)
                if not chunk:
                    break
                total+=len(chunk)
                if total>expected_size or total>limit:
                    raise ValueError('Radio asset exceeds signed size')
                digest.update(chunk)
                file.write(chunk)
            file.flush()
            os.fsync(file.fileno())
        if total!=expected_size or digest.hexdigest()!=expected_hash:
            raise ValueError('Radio asset SHA-256 mismatch')
        return temp
    except Exception:
        temp.unlink(missing_ok=True)
        raise


def sync_world(paths_root, opener=urlopen, require_external=True):
    """Verify current release and install local world snapshot off the GUI."""
    root=Path(paths_root)
    if not world._safe_directory(root) or (
            require_external and root.stat().st_dev == Path('/').stat().st_dev):
        return {'changed':False,'skipped':'unsafe-storage'}
    index=_feed(opener)
    marker=root/world.WORLD_NAME/world.OWNER
    if marker.is_file() and not marker.is_symlink():
        present=world._json_file(marker,world.MAX_OWNER)
        if present.get('archive_sha256')==index['world']['sha256'] and world._owner_ok(marker.parent):
            return {'changed':False,'skipped':'already-current',
                    'countries':present.get('countries')}
    info=index['world']
    archive=_download(opener,_asset(index,info['file']),root,
                      info['sha256'],info['bytes'],ZIP_LIMIT)
    try:
        result=world.install_world(archive,info['sha256'],root,
                                  require_external=require_external)
        if result.get('changed') and result.get('countries')!=index['country_count']:
            raise ValueError('Published country index differs from bundle inventory')
        return result
    finally:
        archive.unlink(missing_ok=True)


def sync_selected_logos(paths_root, enigma_directory, code, opener=urlopen,
                        require_external=True):
    """Fetch only selected country's PNG ZIP, preserve others on failure."""
    root=Path(paths_root)
    if not ISO.fullmatch(code) or not world._safe_directory(root) or (
            require_external and root.stat().st_dev==Path('/').stat().st_dev):
        return {'changed':False,'skipped':'unsafe-selection'}
    bundle=root/world.WORLD_NAME
    marker=bundle/world.OWNER
    if marker.is_symlink() or not marker.is_file():
        return {'changed':False,'skipped':'missing-world'}
    state=world._json_file(marker,world.MAX_OWNER)
    if state.get('owner')!='WarderRadioLive':
        return {'changed':False,'skipped':'unowned-world'}
    if country.active_country(enigma_directory)!=code:
        return {'changed':False,'skipped':'no-longer-selected'}
    feed=_feed(opener)
    if feed['world']['sha256'] != state.get('archive_sha256'):
        return {'changed':False,'skipped':'world-update-needed'}
    info=feed['countries'].get(code)
    if not info or not info['logo_package_complete']:
        return {'changed':False,'skipped':'logos-not-ready'}
    zipinfo=info['logos']
    picon=root/'picon'
    if picon.is_symlink() or not picon.is_dir():
        return {'changed':False,'skipped':'missing-picon-path'}
    current=picon/'radio'
    owner=current/packages.OWNER_FILE
    if current.exists() and not packages._owned_dir(current):
        return {'changed':False,'skipped':'unowned-radio-folder'}
    if owner.is_file() and not owner.is_symlink():
        old=packages._json(owner.read_bytes())
        if (old.get('country')==code and
                old.get('logo_zip_sha256')==zipinfo['sha256']):
            return {'changed':False,'skipped':'already-current'}
    stage=Path(tempfile.mkdtemp(prefix='.warder-country-logo-',dir=str(root)))
    try:
        for group,extension in (('bouquets','radio'),('catalog','json'),
                                ('manifests','json')):
            rel=f'{group}/{code}.{extension}'
            inp=bundle/rel
            if inp.is_symlink() or not inp.is_file():
                return {'changed':False,'skipped':'missing-country'}
            target=stage/rel
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(inp,target)
        source=stage/'logos'
        source.mkdir()
        zipfile=_download(opener,_asset(feed,zipinfo['file']),source,
                          zipinfo['sha256'],zipinfo['bytes'],LOGO_LIMIT)
        os.replace(zipfile,source/(code+'.zip'))
        # If user switched countries during download, never activate stale PNGs.
        if country.active_country(enigma_directory)!=code:
            return {'changed':False,'skipped':'country-superseded'}
        return packages.install_logos(stage,code,picon,
                                      require_external=require_external)
    finally:
        shutil.rmtree(stage)
