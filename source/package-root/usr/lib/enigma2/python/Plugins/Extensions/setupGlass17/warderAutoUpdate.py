"""Fetch startup update metadata in a native child process, never in the GUI."""
import json
import os
import sys
import time
from urllib.request import Request, urlopen

BASE='https://raw.githubusercontent.com/Evolution-by-Warder/FullHDGlass-Warder-Evolution/'
PRODUCTION=BASE+'main/update-production.json'
TEST=BASE+'warder-modernization-work/update-test.json'


def selected_url(version):
    return TEST if '-test' in str(version) else PRODUCTION


def fetch(url):
    if url not in (PRODUCTION,TEST):raise ValueError('Unsafe update manifest URL')
    request=Request(url+'?cb='+str(int(time.time())),headers={'User-Agent':'FullHDGlass-startup-update','Accept':'application/json','Cache-Control':'no-cache, no-store, max-age=0','Pragma':'no-cache'})
    with urlopen(request,timeout=12) as response:
        if response.geturl().split('?',1)[0]!=url:raise ValueError('Unsafe update manifest redirect')
        raw=response.read(16001)
    if len(raw)>16000:raise ValueError('Oversized update manifest')
    result=json.loads(raw.decode('utf-8-sig'))
    if not isinstance(result,dict):raise ValueError('Invalid update manifest')
    return result


class AutoCheck:
    def __init__(self,owner,event_loop=None):
        from .warderHelpPreview import _NativeLoop, _Worker
        self.owner=owner;self.loop=event_loop or _NativeLoop();self.closed=False;self.timeout=None;self.worker=None
        self.url=selected_url(owner.readVersion())
        worker=_Worker(self._finished);self.worker=worker
        try:
            helper=os.path.abspath(__file__)
            self.loop.spawnProcess(worker,'/usr/bin/python3',['/usr/bin/python3',helper,'--fetch',self.url],env=dict(os.environ))
            self.timeout=self.loop.callLater(20,self.close)
        except Exception:
            self._finished(None)

    def _finished(self,manifest):
        self.worker=None
        if self.timeout is not None and self.timeout.active():self.timeout.cancel()
        self.timeout=None
        if self.closed or not isinstance(manifest,dict):return
        if selected_url(self.owner.readVersion())!=self.url:return
        self.owner._warderPreparedManifest=(self.url,manifest)
        # Existing version/SHA/package URL validation, localized offer and user
        # consent remain in the existing screen method, on the GUI thread.
        self.owner.updatechckact(False,automatic=True)

    def close(self):
        self.closed=True
        if self.timeout is not None and self.timeout.active():self.timeout.cancel()
        self.timeout=None
        if self.worker is not None:
            transport=getattr(self.worker,'transport',None)
            try:
                if hasattr(transport,'kill'):transport.kill()
                elif transport is not None:transport.signalProcess('KILL')
            except Exception:pass
        self.worker=None


if __name__=='__main__':
    if len(sys.argv)!=3 or sys.argv[1]!='--fetch':sys.exit(2)
    try:
        os.nice(5)
    except OSError:
        pass
    try:
        print(json.dumps(fetch(sys.argv[2]),ensure_ascii=False))
    except Exception:
        sys.exit(1)
