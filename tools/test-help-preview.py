#!/usr/bin/env python3
"""Exercise the preview queue without an Enigma2 receiver or Twisted install."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
# Isolated stand-ins for reactor events; no background threads or real GUI.
package = types.ModuleType('preview_test_package');package.__path__ = [str(PLUGIN)]
sys.modules[package.__name__] = package
spec = importlib.util.spec_from_file_location('preview_test_package.warderHelpPreview', PLUGIN / 'warderHelpPreview.py')
preview = importlib.util.module_from_spec(spec);spec.loader.exec_module(preview)


class Call:
    def __init__(self, delay, callback):
        self.delay, self.callback, self.pending = delay, callback, True
    def active(self): return self.pending
    def cancel(self): self.pending = False
    def fire(self):
        if self.pending:
            self.pending = False
            self.callback()


class Loop:
    def __init__(self): self.calls = []; self.workers = []; self.fail = False
    def callLater(self, delay, callback):
        call = Call(delay, callback);self.calls.append(call);return call
    def spawnProcess(self, worker, executable, argv, env):
        if self.fail: raise OSError('python unavailable')
        self.workers.append((worker, executable, argv))
        worker.transport = types.SimpleNamespace(signals=[], signalProcess=lambda sig: worker.transport.signals.append(sig))


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.old = preview.cached_path;preview.cached_path = lambda filename: None
        self.shown = [];self.cleared = [];self.loop = Loop()
        self.loader = preview.PreviewLoader(self.shown.append, self.loop, lambda:self.cleared.append(True))
        self.files = patch.object(preview.os.path, 'isfile', return_value=True)
        self.files.start();self.addCleanup(self.files.stop)
    def tearDown(self): preview.cached_path = self.old
    def finish(self, worker, result, code=0):
        if result is not None:
            worker.outReceived(preview.json.dumps(result).encode())
        worker.processEnded(types.SimpleNamespace(value=types.SimpleNamespace(exitCode=code)))

    def test_fast_scrolling_starts_only_last_selection(self):
        for i in range(100): self.loader.request('/picons/%d.png' % i)
        for call in list(self.loop.calls): call.fire()
        self.assertEqual(len(self.loop.workers), 1)
        worker, executable, argv = self.loop.workers[0]
        self.assertEqual(argv[-1], '/picons/99.png')
        self.assertEqual(executable, '/usr/bin/python3')
        self.assertEqual(self.shown, [])
        self.finish(worker, '/picons/99.png')
        self.assertEqual(self.shown, ['/picons/99.png'])

    def test_inflight_worker_never_blocks_navigation_or_displays_stale_selection(self):
        self.loader.request('/a.png');self.loop.calls[-1].fire()
        first = self.loop.workers[0][0]
        for name in ('/b.png', '/c.png', '/d.png'):
            self.loader.request(name);self.loop.calls[-1].fire()
        self.assertEqual(len(self.loop.workers), 1)
        self.assertEqual(self.loader.wanted, '/d.png')
        self.finish(first, '/a.png');self.assertEqual(self.shown, [])
        self.loop.calls[-1].fire();self.assertEqual(len(self.loop.workers), 2)
        self.finish(self.loop.workers[-1][0], '/d.png')
        self.assertEqual(self.shown, ['/d.png'])

    def test_even_cached_archives_are_not_touched_in_the_gui_thread(self):
        def forbidden(filename):raise AssertionError('No filesystem lookup in GUI')
        preview.cached_path = forbidden
        self.loader.request('/a.png');self.loop.calls[-1].fire()
        self.assertEqual(self.shown, []);self.assertEqual(len(self.loop.workers),1)
        self.finish(self.loop.workers[-1][0],'/a.png')
        self.assertEqual(self.shown,['/a.png'])

    def test_close_cancels_queued_work_and_prevents_any_late_widget_call(self):
        self.loader.request('/a.png');self.loop.calls[-1].fire()
        worker = self.loop.workers[-1][0]
        self.loader.request('/b.png');self.loader.close()
        self.assertEqual(worker.transport.signals, ['KILL'])
        self.finish(worker, '/a.png')
        for call in self.loop.calls: call.fire()
        self.assertEqual(self.shown, []);self.assertEqual(len(self.loop.workers), 1)
        self.loader.request('/c.png');self.assertEqual(self.loader.wanted, '/b.png')

    def test_worker_failure_and_missing_interpreter_fall_back_without_exception(self):
        self.loader.request('/a.png');self.loop.calls[-1].fire()
        self.finish(self.loop.workers[-1][0], None, 1)
        self.assertEqual(self.shown, [])
        self.loop.fail = True
        self.loader.request('/b.png');self.loop.calls[-1].fire()
        self.assertEqual(self.shown, [])

    def test_stalled_worker_is_terminated_without_a_blocking_wait(self):
        self.loader.request('/a.png');self.loop.calls[-1].fire()
        timeout = self.loop.calls[-1];self.assertEqual(timeout.delay, 20)
        timeout.fire();worker = self.loop.workers[-1][0]
        self.assertEqual(worker.transport.signals, ['KILL'])
        self.finish(worker, None, 1);self.assertEqual(self.shown, [])

    def test_unexpected_worker_output_cannot_load_an_arbitrary_file(self):
        self.loader.request('/a.png');self.loop.calls[-1].fire()
        self.finish(self.loop.workers[-1][0], '/etc/passwd')
        self.assertEqual(self.shown, [])

    def test_duplicate_selection_does_not_restart_or_repaint(self):
        self.loader.request('/a.png');first = self.loop.calls[-1]
        self.loader.request('/a.png');self.assertIs(self.loop.calls[-1], first)
        first.fire();self.finish(self.loop.workers[-1][0], '/a.png')
        self.loader.request('/a.png');self.assertEqual(self.shown, ['/a.png'])


    def test_missing_next_image_clears_last_successful_image(self):
        self.loader.request('/a.png');self.loop.calls[-1].fire()
        self.finish(self.loop.workers[-1][0], '/a.png')
        self.loader.request('/missing.png');self.loop.calls[-1].fire()
        with patch.object(preview.os.path,'isfile',return_value=False):
            self.finish(self.loop.workers[-1][0], '/missing.png')
        self.assertEqual(self.shown,['/a.png'])
        self.assertEqual(len(self.cleared),3)


class NativeLoopTests(unittest.TestCase):
    def test_native_timer_and_process_drive_preview_without_twisted(self):
        timers=[];containers=[]
        class Timer:
            def __init__(self):self.callback=[];self.stopped=False;timers.append(self)
            def start(self,ms,once):self.ms=ms;self.once=once
            def stop(self):self.stopped=True
            def fire(self):
                for callback in self.callback[:]:callback()
        class Container:
            def __init__(self):self.dataAvail=[];self.appClosed=[];self.killed=False;containers.append(self)
            def execute(self,*args):self.args=args;return 0
            def kill(self):self.killed=True
        native=types.SimpleNamespace(eTimer=Timer,eConsoleAppContainer=Container)
        shown=[]
        with patch.dict(sys.modules,{'enigma':native}),patch.object(preview.os.path,'isfile',return_value=True):
            loader=preview.PreviewLoader(shown.append)
            loader.request('/a.png')
            self.assertEqual(shown,[preview._BLANK])
            self.assertEqual(timers[0].ms,120)
            timers[0].fire()
            self.assertEqual(containers[0].args[:2],('/usr/bin/python3','/usr/bin/python3'))
            containers[0].dataAvail[0](b'"/a.png"')
            containers[0].appClosed[0](0)
            self.assertEqual(shown[-1],'/a.png')
            self.assertTrue(timers[-1].stopped)
            loader.request('/b.png');timers[-1].fire()
            loader.close()
            self.assertTrue(containers[-1].killed)
            containers[-1].appClosed[0](1)
            self.assertEqual(shown[-1],preview._BLANK)


if __name__ == '__main__': unittest.main()
