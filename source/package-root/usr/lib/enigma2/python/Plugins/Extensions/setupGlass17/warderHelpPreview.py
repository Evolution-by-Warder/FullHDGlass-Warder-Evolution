"""Latest-selection preview queue; expensive PNG work runs outside Enigma2.

Only the native Enigma2 GUI event loop touches widgets. A short debounce skips pictures while
scrolling, and at most one low-priority Python worker runs per settings screen.
"""
import json
import os

from .warderHelpArt import cached_path

# Enigma2's own event loop is authoritative on all supported images.
# Import lazily so the queue can also be tested without a receiver.
_BLANK = '/usr/share/enigma2/hd_glass17/buttons/selected-menu_bgpixmap.png'


class _NativeCall:
    def __init__(self, delay, callback):
        from enigma import eTimer
        self.timer = eTimer()
        self.pending = True
        def fire():
            if self.pending:
                self.pending = False
                callback()
        self.callback = fire
        self.timer.callback.append(fire)
        self.timer.start(max(1, int(delay * 1000)), True)

    def active(self):
        return self.pending

    def cancel(self):
        self.pending = False
        self.timer.stop()


class _NativeLoop:
    def callLater(self, delay, callback):
        return _NativeCall(delay, callback)

    def spawnProcess(self, worker, executable, argv, env):
        from enigma import eConsoleAppContainer
        container = eConsoleAppContainer()
        worker.transport = self
        worker.container = container
        def finished(code):
            del container.dataAvail[:]
            del container.appClosed[:]
            worker.complete(code)
            worker.container = None
        container.dataAvail.append(worker.outReceived)
        container.appClosed.append(finished)
        # Native execute accepts executable, argv[0], argv[1]... without a shell.
        result = container.execute(executable, *argv)
        if result:
            raise OSError('Preview worker did not start: %s' % result)
        worker.transport = container


class _Worker:
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
        self.complete(getattr(reason.value, 'exitCode', None))

    def complete(self, code):
        result = None
        if code == 0:
            try:
                result = json.loads(self.output.decode('utf-8'))
            except (ValueError, UnicodeError):
                pass
        self.finished(result)


class PreviewLoader:
    def __init__(self, show, event_loop=None, clear=None):
        self.show = show
        self.loop = event_loop or _NativeLoop()
        self.clear = clear or (lambda: self.show(_BLANK))
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
        self.clear()
        self.wanted = filename
        self.generation += 1
        self._cancel(self.delayed)
        self.delayed = self.loop.callLater(0.12, self._start)

    def _start(self):
        self.delayed = None
        if self.closed or self.process is not None:
            return
        filename, generation = self.wanted, self.generation
        # Even cached ZIP/source lookups may wake a sleeping HDD. Keep all
        # filesystem preparation in the child; only ready local PNGs reach GUI.
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
                transport = self.process.transport
                if hasattr(transport, 'kill'):
                    transport.kill()
                else:
                    transport.signalProcess('KILL')
            except Exception:
                pass

    def _finished(self, generation, filename, result):
        self.process = None
        self._cancel(self.timeout)
        self.timeout = None
        if self.closed:
            return
        if generation == self.generation:
            # A failed load must clear the previous picture, never keep it.
            allowed = isinstance(result, str) and (result == filename or
                (os.path.dirname(result) == '/tmp/warder-help-art-v2' and result.endswith('.png')))
            if allowed and os.path.isfile(result):
                self.show(result)
            else:
                self.clear()
        else:
            self._cancel(self.delayed)
            self.delayed = self.loop.callLater(0, self._start)

    def close(self):
        self.closed = True
        self._cancel(self.delayed)
        self._cancel(self.timeout)
        self._stop_worker()
        self.show = None
