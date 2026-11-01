#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import unittest
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderBitrateCompat.py'
spec=importlib.util.spec_from_file_location('bitrate_compat',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Tests(unittest.TestCase):
    def select(self,**kwargs):
        options={'cpu':'mipsel','exists':lambda path:True,'cpuinfo':'cpu model : MIPS 24Kc V8.1\nisa : mips1 mips2 mips32r1 mips32r2\n','kernel':'3.2.0-vendor','byteorder':'little','targets':{'mipsel':{'isa':'mips32r2','byteorder':'little','minimum_kernel':[3,2],'requires_fpu':False}}}
        options.update(kwargs);return module.select_helper(**options)
    def test_supported_receiver(self):self.assertEqual(self.select(),'/usr/bin/warder-bitrate-mipsel')
    def test_older_cpu_is_not_given_r2_code(self):self.assertEqual(self.select(cpuinfo='isa : mips1 mips2 mips32r1\n'),module.LEGACY)
    def test_older_kernel_is_retained(self):self.assertEqual(self.select(kernel='2.6.18-7.4-dm800'),module.LEGACY)
    def test_unparseable_kernel_and_cpu_are_retained(self):
        self.assertEqual(self.select(kernel='unknown'),module.LEGACY)
        self.assertEqual(self.select(cpuinfo='unknown'),module.LEGACY)
    def test_big_endian_and_r6_are_retained(self):
        self.assertEqual(self.select(byteorder='big'),module.LEGACY)
        self.assertEqual(self.select(cpuinfo='isa : mips32r2 mips32r6\n'),module.LEGACY)
    def test_fpu_requirement_is_enforced_when_toolchain_requires_it(self):
        target={'mipsel':{'isa':'mips32r2','byteorder':'little','minimum_kernel':[3,2],'requires_fpu':True}}
        self.assertEqual(self.select(targets=target),module.LEGACY)
        self.assertEqual(self.select(targets=target,cpuinfo='cpu model : MIPS 24Kf V8.1 FPU V0.0\nisa : mips32r2\n'),'/usr/bin/warder-bitrate-mipsel')
    def test_missing_or_malformed_build_metadata_preserves_legacy(self):
        self.assertEqual(self.select(targets={}),module.LEGACY)
        self.assertEqual(self.select(exists=lambda path:False),module.LEGACY)
    def test_arm_and_sh4(self):
        self.assertEqual(self.select(cpu='arm'),'/usr/bin/warder-bitrate-arm')
        self.assertEqual(self.select(cpu='sh4'),module.LEGACY)
        self.assertEqual(self.select(cpu='aarch64'),'/usr/bin/warder-bitrate-aarch64')
    def test_dreamos_allows_new_external_helpers_but_not_legacy_binary(self):
        self.assertTrue(module.external_helper_available('aarch64',True,exists=lambda path:True))
        self.assertTrue(module.external_helper_available('arm',True,exists=lambda path:True))
        self.assertFalse(module.external_helper_available('sh4',True,exists=lambda path:True))
        self.assertFalse(module.external_helper_available('aarch64',True,exists=lambda path:False))
    def test_short_startup_delay_for_new_helpers(self):
        self.assertEqual(module.startup_delay('arm',False),750)
        self.assertEqual(module.startup_delay('aarch64',True),750)
        self.assertEqual(module.startup_delay('sh4',False),8000)
        self.assertEqual(module.startup_delay('sh4',True),5000)
if __name__=='__main__':unittest.main()
