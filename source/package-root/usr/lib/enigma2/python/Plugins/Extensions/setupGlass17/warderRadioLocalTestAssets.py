"""Exact-SHA local test receiver kit for 224 radio bouquets + selected originals.

Test assets are manually placed once on external PATHS. This is not an online
publisher and does not assert that other 223 original country ZIPs are shipped.
GUI still fetches up-to-date station artwork online if a tested ZIP is absent.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

from . import warderRadioWorld as world
from . import warderRadioPackages as packages
from . import warderRadioCountryBouquets as books

WORLD_SHA='771953b41ceab46f8852f5e3219338cb1369d7f653ed7d329ad551e481f88d68'
BASE='radio-country-test'
WORLD_ARCHIVE='radio-countries-bouquets.zip'
SHA=re.compile(r'^[0-9a-f]{64}$')

def _sha(path):
    d=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(256*1024),b''):d.update(chunk)
    return d.hexdigest()

def test_folder(root):
    root=Path(root)
    if not world._safe_directory(root):return None
    folder=root/BASE
    if folder.is_symlink() or not folder.is_dir():return None
    return folder

def sync_local_world(root,require_external=True):
    root=Path(root);folder=test_folder(root)
    if folder is None:return {'changed':False,'skipped':'missing-local-test-kit'}
    if require_external and root.stat().st_dev==Path('/').stat().st_dev:
        return {'changed':False,'skipped':'unsafe-internal-flash'}
    archive=folder/WORLD_ARCHIVE
    if archive.is_symlink() or not archive.is_file() or archive.stat().st_size>world.MAX_ARCHIVE:
        return {'changed':False,'skipped':'missing-world-archive'}
    if _sha(archive)!=WORLD_SHA:
        raise ValueError('Local 224-country world SHA mismatch')
    return world.install_world(archive,WORLD_SHA,root,
        require_external=require_external,expected_countries=224)

def sync_local_logos(root,directory,code,require_external=True):
    root=Path(root);directory=Path(directory)
    folder=test_folder(root)
    if folder is None or not isinstance(code,str) or not re.fullmatch(r'[A-Z]{2}',code):
        return {'changed':False,'skipped':'missing-local-test-kit'}
    if require_external and root.stat().st_dev==Path('/').stat().st_dev:
        return {'changed':False,'skipped':'unsafe-internal-flash'}
    archive=folder/(code+'.zip')
    if archive.is_symlink() or not archive.is_file():return {
        'changed':False,'skipped':'missing-local-country-originals'}
    from . import warderRadioBundleFetch as fetch
    if not fetch._country_really_selected(directory,code):
        return {'changed':False,'skipped':'no-longer-selected'}
    source=root/world.WORLD_NAME
    marker=source/world.OWNER
    if not world._owner_ok(source):
        return {'changed':False,'skipped':'unverified-external-world'}
    owned=world._json_file(marker,world.MAX_OWNER)
    if owned.get('archive_sha256')!=WORLD_SHA:
        return {'changed':False,'skipped':'test-world-sha-mismatch'}
    index=world._json_file(source/'index.json',world.MAX_INDEX)
    stations=world._verify_index(index)
    meta=stations.get(code)
    if not meta or not meta.get('logo_package_complete'):
        return {'changed':False,'skipped':'missing-country-index'}
    if (_sha(archive)!=meta['logo_sha256'] or
            archive.stat().st_size>packages.MAX_ZIP):
        raise ValueError('Local country original ZIP digest mismatch')
    dest=root/'picon'
    if dest.is_symlink() or (dest.exists() and not dest.is_dir()):
        return {'changed':False,'skipped':'unsafe-external-picon-folder'}
    if not dest.exists():dest.mkdir(mode=0o755)
    tmp=Path(tempfile.mkdtemp(prefix='.warder-radio-local-test-',dir=str(root)))
    try:
        for foldername,ext in (('bouquets','radio'),('catalog','json'),('manifests','json')):
            name=code+'.'+ext
            item=source/foldername/name
            if item.is_symlink() or not item.is_file():
                return {'changed':False,'skipped':'missing-country-files'}
            output=tmp/foldername
            output.mkdir(exist_ok=True)
            shutil.copyfile(item,output/name)
        zips=tmp/'logos'
        zips.mkdir()
        shutil.copyfile(archive,zips/(code+'.zip'))
        # Signed receiver ZIP overrides the internet logo cache, only for
        # the presently selected country, preserving all other picon stores.
        return packages.install_logos(
            tmp,code,dest,require_external=require_external,
            still_selected=lambda current:fetch._country_really_selected(directory,current))
    finally:
        shutil.rmtree(tmp)
