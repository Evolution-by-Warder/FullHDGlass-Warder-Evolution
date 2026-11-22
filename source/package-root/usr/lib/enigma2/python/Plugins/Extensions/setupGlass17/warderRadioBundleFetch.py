"""Background GitHub snapshot downloader for Warder Radio Live.

The public immutable release provides one world-bouquet ZIP and one original
logo ZIP per country. This module never runs in the GUI event loop, and refuses
unpublished/foreign/index-inconsistent data. Country selection itself stays
offline; only snapshots and selected-country logos use HTTP.

TEST-only pre-release source. The production latest.json remains untouched;
the TEST feed uses the isolated Radio-Warder-Evolution feature branch.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import time
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from . import warderRadioWorld as world
from . import warderRadioPackages as packages
from . import warderRadioCountry as country

LATEST_URL = ('https://raw.githubusercontent.com/Evolution-by-Warder/'
              'Radio-Warder-Evolution/feature/radio-browser-country-bouquets-and-logo-zips-20261119/'
              'assets/radio-country/test-20261122.json')
RELEASE_ROOT = ('https://github.com/Evolution-by-Warder/'
                'Radio-Warder-Evolution/releases/download/')
TAG = re.compile(r'^radio-country-20[0-9]{6}$')
ISO = re.compile(r'^[A-Z]{2}$')
SHA = re.compile(r'^[0-9a-f]{64}$')
INDEX_LIMIT = 1024 * 1024
ZIP_LIMIT = world.MAX_ARCHIVE
LOGO_LIMIT = packages.MAX_ZIP
SYNC_STATE = 'warder-radio-world-update.json'
SYNC_PERIOD = 14 * 24 * 3600
SYNC_RETRY = 6 * 3600


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
            data.get('complete') is not True or
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
                record.get('logo_package_complete') is not True or
                (logos.get('asset_tag') is not None and
                 (not isinstance(logos.get('asset_tag'), str) or
                  not TAG.fullmatch(logos['asset_tag']) or
                  logos['asset_tag'] > data['release_tag']))):
            # A global feed cannot claim complete=true while one country's
            # original-logo scan is still pending. Keep last valid snapshot.
            raise ValueError('Incomplete country logo listing')
    return data


def _asset(index, name, asset_tag=None):
    if name not in ('radio-countries-bouquets.zip',) and not (
            re.fullmatch(r'[A-Z]{2}\.zip', name)):
        raise ValueError('Unsafe release asset name')
    if name == 'radio-countries-bouquets.zip':
        if asset_tag is not None:
            raise ValueError('World ZIP must come from current release')
        tag = index['release_tag']
    else:
        tag = index['release_tag'] if asset_tag is None else asset_tag
    if not isinstance(tag, str) or not TAG.fullmatch(tag):
        raise ValueError('Unsafe immutable radio release tag')
    return RELEASE_ROOT + tag + '/' + name


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


def sync_world(paths_root, opener=urlopen, require_external=True,
               state_directory=None, now=None):
    """Verified world update with optional durable, reboot-safe 14-day cadence.

    Only the subprocess passes state_directory=/etc/enigma2. Existing offline
    callers and unit tests may omit it and run an explicit forced check.
    """
    root=Path(paths_root)
    if not world._safe_directory(root) or (
            require_external and root.stat().st_dev == Path('/').stat().st_dev):
        return {'changed':False,'skipped':'unsafe-storage'}
    now = time.time() if now is None else now
    state_path = None
    if state_directory is not None:
        parent = Path(state_directory)
        state_path = parent / SYNC_STATE
        if (parent.is_symlink() or not parent.is_dir() or
                not packages.live._safe_file(state_path)):
            return {'changed':False,'skipped':'unsafe-state'}
        if now < 1700000000:
            return {'changed':False,'skipped':'clock','retry_after':3600}
        state = packages.live._read_json(state_path,{},4096)
        if not isinstance(state,dict):
            state = {}
        prev = state.get('last_success')
        attempt = state.get('last_attempt')
        # A cached snapshot may have been removed between GUI restarts.
        # Never suppress re-download when the active local snapshot is absent.
        have_world = (root / world.WORLD_NAME / world.OWNER).is_file()
        if have_world and type(prev) in (int,float) and 0 <= now-prev < SYNC_PERIOD:
            return {'changed':False,'skipped':'not-due',
                    'retry_after':max(60,int(SYNC_PERIOD-(now-prev)))}
        if type(attempt) in (int,float) and 0 <= now-attempt < SYNC_RETRY:
            return {'changed':False,'skipped':'not-due',
                    'retry_after':max(60,int(SYNC_RETRY-(now-attempt)))}
        state['last_attempt'] = now
        packages.live._write(state_path,packages.live._json_bytes(state))
    index=_feed(opener)
    marker=root/world.WORLD_NAME/world.OWNER
    if marker.is_file() and not marker.is_symlink():
        present=world._json_file(marker,world.MAX_OWNER)
        owned=world._owner_ok(marker.parent)
        if owned:
            # The publisher also reviews removals, but a bad future
            # latest.json must never erase a working cached country.
            previous=world._json_file(marker.parent/'index.json',world.MAX_INDEX)
            previous_codes=set(world._verify_index(previous))
            removed=sorted(previous_codes-set(index['countries']))
            if removed:
                return {'changed':False,
                        'skipped':'country-removal-requires-review',
                        'removed_countries':removed}
        if present.get('archive_sha256')==index['world']['sha256'] and owned:
            result={'changed':False,'skipped':'already-current',
                    'countries':present.get('countries')}
        else:
            result=None
    else:
        result=None
    if result is None:
        info=index['world']
        archive=_download(opener,_asset(index,info['file']),root,
                          info['sha256'],info['bytes'],ZIP_LIMIT)
        try:
            result=world.install_world(
                archive,info['sha256'],root,
                require_external=require_external,
                expected_countries=index['country_count'])
        finally:
            archive.unlink(missing_ok=True)
    if state_path is not None and (
            result.get('changed') or result.get('skipped') == 'already-current'):
        state['last_success'] = now
        state['last_sha256'] = index['world']['sha256']
        packages.live._write(state_path,packages.live._json_bytes(state))
    return result


def _country_really_selected(enigma_directory, code):
    """Only the saved or OSD-default ACTIVE single-country bouquet owns logos."""
    return country.active_country(enigma_directory) == code


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
    if not _country_really_selected(enigma_directory, code):
        return {'changed':False,'skipped':'no-longer-selected'}
    feed=_feed(opener)
    if feed['world']['sha256'] != state.get('archive_sha256'):
        return {'changed':False,'skipped':'world-update-needed'}
    info=feed['countries'].get(code)
    if not info or not info['logo_package_complete']:
        return {'changed':False,'skipped':'logos-not-ready'}
    zipinfo=info['logos']
    picon=root/'picon'
    if picon.is_symlink() or (picon.exists() and not picon.is_dir()):
        return {'changed':False,'skipped':'unsafe-picon-path'}
    if not picon.exists():
        # Only the background worker may create the standard PATHS/picon
        # parent; the dedicated picon/radio directory is created by the
        # verified logo installer and never on the GUI event loop.
        try:
            picon.mkdir(mode=0o755)
        except (OSError, FileExistsError):
            return {'changed':False,'skipped':'missing-picon-path'}
    if picon.is_symlink() or not picon.is_dir() or (
            require_external and picon.stat().st_dev == Path('/').stat().st_dev):
        return {'changed':False,'skipped':'unsafe-picon-path'}
    current=picon/'radio'/code
    if not packages._owned_country_dir(current, code):
        return {'changed':False,'skipped':'user-modified-country-picons'}
    owner=current/packages.COUNTRY_APPROVED_OWNER
    if owner.is_file() and not owner.is_symlink():
        old=packages._json(owner.read_bytes())
        if (old.get('country')==code and
                old.get('logo_zip_sha256')==zipinfo['sha256']):
            return {'changed':False,'skipped':'already-current',
                    'country':code,'logos':len(old.get('files', {}))}
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
        zipfile=_download(opener,_asset(feed,zipinfo['file'],
                                       zipinfo.get('asset_tag')),source,
                          zipinfo['sha256'],zipinfo['bytes'],LOGO_LIMIT)
        os.replace(zipfile,source/(code+'.zip'))
        # If user switched countries during download, never activate stale PNGs.
        if not _country_really_selected(enigma_directory, code):
            return {'changed':False,'skipped':'country-superseded'}
        return packages.install_country_logos(
            stage, code, picon, require_external=require_external,
            still_selected=lambda selected:
                _country_really_selected(enigma_directory, selected))
    finally:
        shutil.rmtree(stage)
