#!/usr/bin/env python3
"""Exercise actual infobar methods using Enigma2's documented argv convention."""
import ast
import importlib.util
from pathlib import Path
from types import SimpleNamespace as NS
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py'
source = PLUGIN.read_text()
module = ast.parse(source)
original = next(n for n in module.body if isinstance(n, ast.ClassDef) and n.name == 'ExtraInfo17')
names = {'__startBitrate', 'dataAvail', 'bitrateSample', 'bitrateClosed', 'bitrateTimedOut', 'stopBitrateNow', 'restartBtrStop', 'updBtrData', 'waitBitrateReady'}
methods = [n for n in original.body if isinstance(n, ast.FunctionDef) and n.name in names]
assert len(methods) == len(names)
class_node = ast.ClassDef(name='Runtime', bases=[], keywords=[], body=methods, decorator_list=[])
class_module = ast.fix_missing_locations(ast.Module(body=[class_node], type_ignores=[]))
settings = NS(par35=NS(value='9999999'), par25=NS(value=False), par115=NS(value='0'))
logs = []
compat_path=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderBitrateCompat.py'
spec=importlib.util.spec_from_file_location('bitrate_compat_runtime',compat_path);compat=importlib.util.module_from_spec(spec);spec.loader.exec_module(compat)
def choose_helper(cpu,exists):
    return compat.select_helper(cpu,exists=exists,cpuinfo='isa : mips32r1 mips32r2\n',kernel='3.2.0',byteorder='little',targets={'mipsel':{'isa':'mips32r2','byteorder':'little','minimum_kernel':[3,2,0],'requires_fpu':False}})
def can_external(cpu, restricted, exists):
    helper=choose_helper(cpu,exists)
    return exists(helper) and (helper!=compat.LEGACY or not restricted)
namespace = {'external_helper_available':can_external, 'config': NS(plugins=NS(setupGlass17=settings)), '_': lambda s:s,
             'select_helper':choose_helper, 'ENAEBTR': False, 'ENA_Z': False, 'XCPU':'arm', 'fileExists':lambda p:True,
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
    def start(self, milliseconds, single=False): self.active = milliseconds
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
        namespace['ENAEBTR'] = False
        namespace['ENA_Z'] = False
        namespace['fileExists'] = lambda path:True
        settings.par25.value = False; settings.par35.value = '9999999'
    def running(self):
        obj = Harness({'adapter':1,'demux':3}); obj.start(); return obj
    def test_arm_arguments_reach_helper_in_order(self):
        obj = self.running()
        self.assertEqual(obj.container.argv, ('/usr/bin/warder-bitrate-arm','1','3','7297','7298'))
        self.assertFalse(obj.bitNotActive)
    def test_missing_arm_helper_fails_without_executing_mips_binary(self):
        namespace['fileExists'] = lambda path:path!='/usr/bin/warder-bitrate-arm'
        obj = Harness({'adapter':1,'demux':3});obj.container.result=-1;obj.start()
        self.assertIsNone(obj.container.args)
        self.assertEqual(obj.label.text,'Bitrate failed')
    def test_legacy_helpers_do_not_receive_adapter(self):
        namespace['fileExists'] = lambda path:path!='/usr/bin/warder-bitrate-mipsel'
        for cpu in ('mipsel', 'sh4'):
            namespace['XCPU'] = cpu
            obj = self.running()
            self.assertEqual(obj.container.argv, ('/usr/bin/btrGen17','3','7297','7298'))
    def test_new_mips_helper_receives_adapter_and_demux(self):
        namespace['XCPU']='mipsel'
        obj=self.running()
        self.assertEqual(obj.container.argv,('/usr/bin/warder-bitrate-mipsel','1','3','7297','7298'))
    def test_missing_stream_metadata_waits_without_starting_wrong_demux(self):
        for obj in (Harness(), Harness(stream_error=True)):
            obj.start()
            self.assertIsNone(obj.container.args)
            self.assertEqual(obj.runBitTimer.active,250)
            self.assertTrue(obj.bitNotActive)
    def test_readiness_wait_is_bounded(self):
        obj=Harness()
        for _ in range(21):obj.start()
        self.assertIsNone(obj.container.args)
        self.assertEqual(obj.label.text,'Bitrate failed')
    def test_mismatched_pmt_pid_is_not_started(self):
        obj=Harness({'adapter':0,'demux':0,'pids':[(8000,'video'),(7298,'audio')]})
        obj.start();self.assertIsNone(obj.container.args)
        self.assertEqual(obj.label.text,'Preparing Bitrate')
    def test_zero_initial_video_does_not_replace_starting_with_zero(self):
        obj=self.running();obj.dataAvail(b'0 0 0 0\n1 2 3 159\n')
        self.assertEqual(obj.label.text,'Starting Bitrate')
        self.assertTrue(obj.bitrateStartTimer.active)
        obj.dataAvail(b'10 20 30 8000\n1 2 3 159\n')
        self.assertEqual(obj.label.text,'Btr: V: 8000 kb/s, A: 159 kb/s')
        self.assertFalse(obj.bitrateStartTimer.active)
    def test_aarch64_dreamos_external_helper_arguments(self):
        namespace['XCPU']='aarch64';namespace['ENA_Z']=True
        obj=self.running()
        self.assertEqual(obj.container.argv,('/usr/bin/warder-bitrate-aarch64','1','3','7297','7298'))
    def test_native_failure_can_use_available_external_helper(self):
        namespace['ENAEBTR']=True;namespace['ENAEBTR2']=False
        def fail(*args):raise TypeError('unsupported native calculator ABI')
        namespace['eBitrateCalculator']=fail
        obj=Harness({'adapter':1,'demux':3})
        obj.session.nav.getCurrentlyPlayingServiceReference=lambda:NS(getPath=lambda:'',getData=lambda n:1,toString=lambda:'1:0:1:1:2:3:0:0:0:0:')
        obj.start()
        self.assertEqual(obj.container.argv,('/usr/bin/warder-bitrate-arm','1','3','7297','7298'))
    def test_launch_failure_is_visible_and_not_marked_running(self):
        obj = Harness({'adapter':0,'demux':0}); obj.container.result = -1; obj.start()
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
