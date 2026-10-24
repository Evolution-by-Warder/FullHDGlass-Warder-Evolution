"""Latest-selection preview queue; expensive PNG work runs outside Enigma2.

Only the reactor thread touches widgets. A short debounce skips pictures while
scrolling, and at most one low-priority Python worker runs per settings screen.
"""
import json
import os

from twisted.internet import reactor
from twisted.internet.protocol import ProcessProtocol

from .warderHelpArt import cached_path


class _Worker(ProcessProtocol):
    def __init__(self, finished):
        self.finished = finished
        self.output = bytearray()

    def outReceived(self, data):
        # The worker returns only one filename, never image bytes or a log.
        if len(self.output) + len(data) <= 16384:
            self.output.extend(data)

    def errReceived(self, data):
        pass

    def processEnded(self, reason):
        result = None
        if getattr(reason.value, 'exitCode', None) == 0:
            try:
                result = json.loads(self.output.decode('utf-8'))
            except (ValueError, UnicodeError):
                pass
        self.finished(result)


class PreviewLoader:
    def __init__(self, show, event_loop=None):
        self.show = show
        self.loop = event_loop or reactor
        self.closed = False
        self.wanted = None
        self.generation = 0
        self.delayed = None
        self.process = None
        self.timeout = None

    @staticmethod
    def _cancel(call):
        if call is not None and call.active():
            call.cancel()

    def request(self, filename):
        if self.closed or filename == self.wanted:
            return
        self.wanted = filename
        self.generation += 1
        self._cancel(self.delayed)
        self.delayed = self.loop.callLater(0.12, self._start)

    def _start(self):
        self.delayed = None
        if self.closed or self.process is not None:
            return
        filename, generation = self.wanted, self.generation
        ready = cached_path(filename)
        if ready is not None:
            self.show(ready)
            return
        worker = _Worker(lambda result: self._finished(generation, filename, result))
        self.process = worker
        try:
            # sys.executable may point to /usr/bin/enigma2 in embedded Python.
            # Use the image's Python 3 interpreter, with argv and no shell.
            helper = os.path.join(os.path.dirname(__file__), 'warderHelpArt.py')
            self.loop.spawnProcess(worker, '/usr/bin/python3',
                                   ['/usr/bin/python3', helper, '--prepare', filename],
                                   env=dict(os.environ))
            self.timeout = self.loop.callLater(20, self._stop_worker)
        except Exception:
            self._finished(generation, filename, None)

    def _stop_worker(self):
        if self.process is not None:
            try:
                self.process.transport.signalProcess('KILL')
            except Exception:
                pass

    def _finished(self, generation, filename, result):
        self.process = None
        self._cancel(self.timeout)
        self.timeout = None
        if self.closed:
            return
        if generation == self.generation:
            # Accept only the source or an existing PNG in our own cache.
            if not isinstance(result, str) or (result != filename and
                    (os.path.dirname(result) != '/tmp/warder-help-art-v2' or
                     not result.endswith('.png') or not os.path.isfile(result))):
                result = filename
            self.show(result)
        else:
            self._cancel(self.delayed)
            self.delayed = self.loop.callLater(0, self._start)

    def close(self):
        self.closed = True
        self._cancel(self.delayed)
        self._cancel(self.timeout)
        self._stop_worker()
        self.show = None
