"""Verified optional previews from the shared auxiliary download structure."""
import hashlib
import json
import os
import tempfile
import threading
import urllib.request

_ENV='WARDER_FHD_PREVIEW_CACHE'
_ROOT='/var/cache/warder-fullhdglass/previews'
_MANIFEST=None
_LOCK=threading.Lock()
_RUNNING=False


def manifest():
    global _MANIFEST
    if _MANIFEST is None:
        with open(os.path.join(os.path.dirname(__file__),'preview-assets.json')) as stream:
            _MANIFEST=json.load(stream)
    return _MANIFEST


def bundle_path(kind):
    entry=manifest()[kind]
    return os.path.join(os.environ.get(_ENV,_ROOT),entry['sha256']+'-'+entry['filename'])


class _Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        from urllib.parse import urlparse
        parsed=urlparse(newurl)
        if parsed.scheme!='https' or parsed.hostname not in ('github.com','release-assets.githubusercontent.com','objects.githubusercontent.com','raw.githubusercontent.com'):
            raise ValueError('Untrusted preview redirect')
        return super().redirect_request(request,fp,code,msg,headers,newurl)


def _valid(path,entry):
    try:
        if os.path.getsize(path)!=entry['size']:return False
        digest=hashlib.sha256()
        with open(path,'rb') as stream:
            for chunk in iter(lambda:stream.read(131072),b''):digest.update(chunk)
        return digest.hexdigest()==entry['sha256']
    except OSError:return False


def _download(kind,opener=None):
    entry=manifest()[kind];target=bundle_path(kind)
    if _valid(target,entry):return target
    allowed={
        'help':'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/ui/help/g17_setup_pict.zip',
        'types':'https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/main/assets/warder/downloads/ui/icon-set-previews/warder-infobar-types.zip',
    }
    if entry['url']!=allowed.get(kind):raise ValueError('Untrusted preview source')
    folder=os.path.dirname(target)
    if os.path.basename(folder)=='.warder-previews' and not os.path.isdir(os.path.dirname(folder)):
        raise OSError('Selected preview storage is unavailable')
    os.makedirs(folder,mode=0o700,exist_ok=True)
    handle,temporary=tempfile.mkstemp(prefix='.download-',dir=folder)
    try:
        request=urllib.request.Request(entry['url'],headers={'User-Agent':'FullHDGlass-previews'})
        opener=opener or urllib.request.build_opener(_Redirect())
        with os.fdopen(handle,'wb') as output:
            with opener.open(request,timeout=15) as response:
                size=0
                while True:
                    chunk=response.read(131072)
                    if not chunk:break
                    size+=len(chunk)
                    if size>entry['size']:raise ValueError('Preview archive is oversized')
                    output.write(chunk)
        if not _valid(temporary,entry):raise ValueError('Preview checksum mismatch')
        os.replace(temporary,target)
        return target
    finally:
        if os.path.exists(temporary):os.unlink(temporary)


def _prepare():
    global _RUNNING
    try:
        for kind in ('types','help'):
            try:
                _download(kind)
                if kind=='types':
                    from .warderTypePreviews import prepare_bundle
                    prepare_bundle()
            except Exception:pass  # Optional offline assets must not flood Enigma2 logs.
    finally:
        with _LOCK:_RUNNING=False


def ensure_assets(storage_root=None):
    """Return immediately; retry missing assets on the next settings opening."""
    global _RUNNING
    with _LOCK:
        if _RUNNING:return
        if storage_root:os.environ[_ENV]=os.path.join(str(storage_root),'.warder-previews')
        _RUNNING=True
    try:
        thread=threading.Thread(target=_prepare,name='FullHDGlass-previews',daemon=True)
        thread.start()
    except Exception:
        with _LOCK:_RUNNING=False
