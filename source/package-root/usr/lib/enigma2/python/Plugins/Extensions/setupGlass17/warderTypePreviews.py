"""Small, prepared type previews; no full screenshot decoding in the list."""
import os
import tempfile
import zipfile
from functools import lru_cache

from .warderPreviewAssets import bundle_path, manifest
_BUNDLE=None


@lru_cache(maxsize=1)
def _cache_dir():
    revision=manifest()['types']['sha256'][:16]
    folder=os.path.join(tempfile.gettempdir(),'warder-infobar-types-'+revision)
    os.makedirs(folder,mode=0o700,exist_ok=True)
    return folder


def thumbnail_path(type_id):
    """Only RAM-backed local cache probes; never open an HDD archive in GUI."""
    try:
        target=os.path.join(_cache_dir(),'type-%d.png'%int(type_id))
        return target if os.path.isfile(target) else ''
    except (OSError,ValueError,KeyError):return ''


def prepare_bundle():
    """Called by the background downloader, never from a screen callback."""
    folder=_cache_dir()
    with zipfile.ZipFile(_BUNDLE or bundle_path('types')) as source:
        for entry in source.infolist():
            name=entry.filename
            if not name.startswith('type-') or not name.endswith('.png') or not name[5:-4].isdigit() or entry.file_size>128*1024:
                raise ValueError('Unexpected type thumbnail')
            target=os.path.join(folder,name)
            if os.path.isfile(target):continue
            handle,temp_path=tempfile.mkstemp(prefix='.type-',dir=folder)
            try:
                with os.fdopen(handle,'wb') as stream:stream.write(source.read(entry))
                os.replace(temp_path,target)
            finally:
                if os.path.exists(temp_path):os.unlink(temp_path)
