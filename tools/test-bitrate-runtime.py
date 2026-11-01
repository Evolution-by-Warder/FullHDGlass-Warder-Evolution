#!/usr/bin/env python3
"""Exercise actual infobar methods using Enigma2's documented argv convention."""
import ast
from pathlib import Path
from types import SimpleNamespace as NS
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py'
source = PLUGIN.read_text()
module = ast.parse(source)
original = next(n for n in module.body if isinstance(n, ast.ClassDef) and n.name == 'ExtraInfo17')
names = {'__startBitrate', 'dataAvail', 'bitrateSample', 'bitrateClosed', 'bitrateTimedOut', 'stopBitrateNow', 'restartBtrStop', 'updBtrData'}
methods = [n for n in original.body if isinstance(n, ast.FunctionDef) and n.name in names]
assert len(methods) == len(names)
class_node = ast.ClassDef(name='Runtime', bases=[], keywords=[], body=methods, decorator_list=[])
class_module = ast.fix_missing_locations(ast.Module(body=[class_node], type_ignores=[]))
settings = NS(par35=NS(value='9999999'), par25=NS(value=False), par115=NS(value='0'))
logs = []
namespace = {'config': NS(plugins=NS(setupGlass17=settings)), '_': lambda s:s,
             'ENAEBTR': False, 'ENA_Z': False, 'XCPU':'arm', 'fileExists':lambda p:True,
             'iServiceInformation':NS(sVideoPID=0, sAudioPID=1), 'Writelog':logs.append, 'BitrateDiagnostic':lambda *args:NS(record=lambda *args,**kw:None, sample=lambda *args:None)}
exec(compile(class_module, str(PLUGIN), 'exec'), namespace)
Runtime = namespace['Runtime']

class Label:
    def __init__(self): self.text = ''
    def setText(self, text): self.text = text
    def __getattr__(self, name): return lambda *args:None
class Timer:
    def __init__(self): self.active = False
    def stop(self): self.active = False
    def isActive(self): return self.active
    def startLongTimer(self, seconds): self.active = seconds
class Console:
    def __init__(self): self.args = None; self.alive = False; self.result = 0
    def execute(self, *args):
        self.args = args
        # python_console.i calls execute(argv[0], argv+1), then execvp.
        self.argv = args[1:]
        self.alive = not bool(self.result)
        return self.result
    def running(self): return self.alive
    def kill(self): self.alive = False
class Harness(Runtime):
    def __init__(self, streamdata=None, stream_error=False):
        self.label = Label()
        self.runBitTimer = Timer(); self.bitrateStartTimer = Timer(); self.restartBtrTimer = Timer()
        self.bitNotActive = True; self.isBit = False; self.numBit = 0
        self.dataV = self.dataA = 0
        self.container = Console()
        def stream():
            if stream_error: raise RuntimeError('stream unavailable')
            return NS(getStreamingData=lambda:streamdata)
        self.session = NS(nav=NS(getCurrentService=lambda:NS(info=lambda:NS(getInfo=lambda pid:(7297,7298)[pid]), stream=stream)))
    def __getitem__(self, name): return self.label
    def start(self): self._Runtime__startBitrate()

class BitrateTests(unittest.TestCase):
    def setUp(self):
        namespace['XCPU'] = 'arm'
        settings.par25.value = False; settings.par35.value = '9999999'
    def running(self):
        obj = Harness({'adapter':1,'demux':3}); obj.start(); return obj
    def test_arm_arguments_reach_helper_in_order(self):
        obj = self.running()
        self.assertEqual(obj.container.argv, ('/usr/bin/btrGen17','1','3','7297','7298'))
        self.assertFalse(obj.bitNotActive)
    def test_mips_and_sh4_do_not_receive_adapter(self):
        for cpu in ('mipsel', 'sh4'):
            namespace['XCPU'] = cpu
            obj = self.running()
            self.assertEqual(obj.container.argv, ('/usr/bin/btrGen17','3','7297','7298'))
    def test_missing_stream_metadata_does_not_crash(self):
        for obj in (Harness(), Harness(stream_error=True)):
            obj.start()
            self.assertEqual(obj.container.argv, ('/usr/bin/btrGen17','0','2','7297','7298'))
    def test_launch_failure_is_visible_and_not_marked_running(self):
        obj = Harness(); obj.container.result = -1; obj.start()
        self.assertEqual(obj.label.text, 'Bitrate failed')
        self.assertTrue(obj.bitNotActive); self.assertFalse(obj.isBit)
        self.assertFalse(obj.bitrateStartTimer.active)
    def test_early_helper_exit_does_not_leave_starting_message(self):
        obj = self.running(); obj.container.alive = False; obj.bitrateClosed(1)
        self.assertEqual(obj.label.text, 'Bitrate failed'); self.assertFalse(obj.isBit)
    def test_no_data_startup_deadline(self):
        obj = self.running(); self.assertEqual(obj.bitrateStartTimer.active, 20)
        obj.bitrateTimedOut()
        self.assertEqual(obj.label.text, 'Bitrate failed'); self.assertFalse(obj.container.alive)
    def test_bytes_can_be_split_at_every_boundary(self):
        sample = b'1000 9000 5000 4500\n64 256 192 128\n'
        for split in range(len(sample)+1):
            obj = self.running(); obj.dataAvail(sample[:split]); obj.dataAvail(sample[split:])
            self.assertEqual(obj.label.text, 'Btr: V: 4500 kb/s, A: 128 kb/s', split)
            self.assertFalse(obj.bitrateStartTimer.active)
    def test_text_multiple_frames_and_flexible_whitespace(self):
        obj = self.running()
        obj.dataAvail('1 2 3 4\n5 6 7 8\n  10\t20  30 40\r\n50 60 70 80\r\n')
        self.assertEqual(obj.label.text, 'Btr: V: 40 kb/s, A: 80 kb/s')
    def test_diagnostics_and_partial_line_do_not_publish_fake_rates(self):
        obj = self.running(); obj.dataAvail(b'usage: invalid parameters\n1 2 3')
        self.assertEqual(obj.label.text, 'Starting Bitrate')
        self.assertTrue(obj.bitrateStartTimer.active)
    def test_full_statistics_keep_video_audio_columns(self):
        settings.par25.value = True
        obj = self.running()
        expected = {0: 'Act: V: 4 kb/s, A: 8 kb/s',2:'Avg: V: 3 kb/s, A: 7 kb/s',4:'Min: V: 1 kb/s, A: 5 kb/s',6:'Max: V: 2 kb/s, A: 6 kb/s'}
        for index, text in expected.items():
            obj.numBit=index; obj.dataAvail(b'1 2 3 4\n5 6 7 8\n'); self.assertEqual(obj.label.text,text)
    def test_limit_and_intentional_stop_clear_state_and_timers(self):
        obj = self.running(); settings.par35.value = '4000'
        obj.dataAvail(b'1 2 3 4500\n5 6 7 8\n')
        self.assertEqual(obj.label.text,'Btr: too high - stopped')
        obj.bitrateClosed(-9)
        self.assertEqual(obj.label.text,'Btr: too high - stopped')
        self.assertFalse(obj.restartBtrTimer.active); self.assertFalse(obj.bitrateStartTimer.active)
        obj.dataAvail(b'1 2 3 4\n5 6 7 8\n'); self.assertFalse(obj.isBit)
    def test_buffer_is_bounded(self):
        obj = self.running(); obj.dataAvail('x'*5000)
        self.assertEqual(obj.bitrateBuffer,'')

if __name__ == '__main__': unittest.main()
