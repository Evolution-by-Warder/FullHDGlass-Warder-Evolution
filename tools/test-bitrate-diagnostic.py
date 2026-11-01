#!/usr/bin/env python3
from pathlib import Path
from types import SimpleNamespace as NS
import importlib.util
import json
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderBitrateDiagnostic.py'
spec=importlib.util.spec_from_file_location('bitrate_diag',p); module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Tests(unittest.TestCase):
    def test_exact_launch_and_live_pids_and_zero_sample(self):
        with tempfile.TemporaryDirectory() as d:
            path=str(Path(d)/'log.json')
            diag=module.BitrateDiagnostic(1210,1220,['/absent-helper','0','2','1210','1220'],{'adapter':0,'demux':2,'url':'private'},path)
            service=NS(info=lambda:NS(getInfo=lambda key:(1211,1220)[key]),stream=lambda:NS(getStreamingData=lambda:{'adapter':0,'demux':3}))
            diag.record('raw',text='0 0 0 0\n64 256 192 159\n')
            diag.sample(['0']*4,['64','256','192','159'],service,NS(sVideoPID=0,sAudioPID=1))
            data=json.loads(Path(path).read_text())
            self.assertEqual(data['video_pid'],1210)
            self.assertEqual(data['events'][-1]['video_pid_now'],1211)
            self.assertEqual(data['events'][-1]['video'],['0']*4)
            self.assertEqual(data['events'][-1]['stream_now']['demux'],3)
            self.assertNotIn('url',data['stream'])
            self.assertEqual(Path(path).stat().st_mode&0o777,0o600)
    def test_cap_and_missing_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            path=str(Path(d)/'log.json')
            diag=module.BitrateDiagnostic(-1,100,['/absent-helper'],None,path)
            for n in range(100):diag.sample(['0']*4,['1']*4,None,NS())
            data=json.loads(Path(path).read_text())
            self.assertEqual(len(data['events']),module.LIMIT)
            self.assertLess(Path(path).stat().st_size,20000)
    def test_write_failure_does_not_break_measurement(self):
        diag=module.BitrateDiagnostic(1,2,['/absent-helper'],{},'/absent-parent/log.json')
        diag.record('raw',text='1 2 3 4\n')
        self.assertEqual(len(diag.events),2)
if __name__=='__main__':unittest.main()
