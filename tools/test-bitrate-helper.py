#!/usr/bin/env python3
"""Run the actual C helper against a userspace DVB syscall simulator."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
class HelperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(); cls.folder=Path(cls.tmp.name)
        source=ROOT/'tools/bitrate-helper'
        cls.binary=cls.folder/'helper';cls.mock=cls.folder/'mock.so'
        subprocess.run(['gcc','-std=c99','-O2','-Wall','-Wextra','-Werror',str(source/'warder-bitrate.c'),'-o',str(cls.binary)],check=True)
        subprocess.run(['gcc','-shared','-fPIC','-O2','-Wall','-Wextra','-Werror',str(source/'mock-dvb.c'),'-o',str(cls.mock),'-ldl'],check=True)
        unit=cls.folder/'unit'
        subprocess.run(['gcc','-std=c99','-O2','-Wall','-Wextra','-Wno-unused-function',str(source/'unit.c'),'-o',str(unit)],check=True)
        subprocess.run([str(unit)],check=True)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def run_helper(self, env=None, seconds=2.3, pids=('5101','5106')):
        environ=os.environ.copy();environ['LD_PRELOAD']=str(self.mock);environ.update(env or {})
        process=subprocess.Popen([str(self.binary),'0','0',*pids],env=environ,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:out,err=process.communicate(timeout=seconds)
        except subprocess.TimeoutExpired:
            process.terminate();out,err=process.communicate(timeout=2)
        rows=[list(map(int,row.split())) for row in out.splitlines()]
        self.assertTrue(all(len(row)==4 for row in rows))
        self.assertEqual(len(rows)%2,0)
        return process.returncode,rows,err
    def test_video_uses_ts_from_first_sample_with_audio_still_measured(self):
        code,rows,err=self.run_helper(seconds=2.3)
        self.assertEqual(code,0,err);self.assertGreaterEqual(len(rows),4)
        self.assertTrue(all(row[3]>0 for row in rows),rows)
        self.assertIn('pid=5101 mode=ts',err)
        self.assertIn('pid=5106 mode=pes',err)
        self.assertNotIn('switching',err)
    def test_pes_only_driver_is_retained(self):
        code,rows,err=self.run_helper({'MOCK_TS_FAIL':'1','MOCK_VIDEO_PES':'1'})
        self.assertEqual(code,0,err);self.assertTrue(rows)
        self.assertTrue(all(row[3]>0 for row in rows))
        self.assertIn('mode=ts: Operation not supported',err)
        self.assertIn('pid=5101 mode=pes adapter=',err)
    def test_legacy_pes_failure_does_not_delay_ts_measurement(self):
        code,rows,err=self.run_helper({'MOCK_PES_FAIL':'1'},seconds=1.3)
        self.assertEqual(code,0,err);self.assertGreater(rows[0][3],0)
        self.assertIn('pid=5101 mode=ts',err)
    def test_unsupported_filters_report_failure(self):
        code,rows,err=self.run_helper({'MOCK_PES_FAIL':'1','MOCK_TS_FAIL':'1'},seconds=1)
        self.assertEqual(code,2);self.assertFalse(rows);self.assertIn('mode=ts: Operation not supported',err)
    def test_audio_only_service_does_not_open_invalid_video_pid(self):
        code,rows,err=self.run_helper(pids=('-1','5106'),seconds=1.3)
        self.assertEqual(code,0,err);self.assertEqual(rows[0],[0,0,0,0]);self.assertGreater(rows[1][3],0)
        self.assertNotIn('pid=-1',err)
    def test_bad_arguments_fail_before_opening_filters(self):
        result=subprocess.run([str(self.binary),'0','0','8191','5106'],capture_output=True,text=True)
        self.assertEqual(result.returncode,2);self.assertIn('usage:',result.stderr)
if __name__=='__main__':unittest.main()
