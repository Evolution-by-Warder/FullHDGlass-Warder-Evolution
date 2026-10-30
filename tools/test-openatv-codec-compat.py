"""Verify the real image codec resolver on current, legacy and unknown images."""
from pathlib import Path
from types import ModuleType
import importlib.util,sys,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location('warder_codec_test',ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderVideoCodec.py');codec=importlib.util.module_from_spec(s);s.loader.exec_module(codec)
def modules(modern=None,legacy=None):
 d={}
 for name in ('Components','Components.SystemInfo','Components.Converter','Components.Converter.PliExtraInfo'):d[name]=ModuleType(name)
 if modern is not None:d['Components.SystemInfo'].VideoCodec=modern
 if legacy is not None:d['Components.Converter.PliExtraInfo'].codec_data=legacy
 return d
class CodecTests(unittest.TestCase):
 def test_current_image_table_and_new_avs2_are_used_before_legacy_fallback(self):
  class Table:
   @staticmethod
   def getName(value,default=''):return {7:'HEVC',9:'VP9',40:'AVS2'}.get(value,default)
  with patch.dict(sys.modules,modules(Table,{7:'wrong'})):
   self.assertEqual([codec.image_codec_name(x) for x in (7,9,40,-1,999)],['HEVC','VP9','AVS2','',''])
 def test_legacy_mapping_retained_without_current_table(self):
  with patch.dict(sys.modules,modules(legacy={7:'HEVC',9:'VP9',5:'bad/type'})):
   self.assertEqual([codec.image_codec_name(x) for x in (7,9,5,99)],['HEVC','VP9','',''])
 def test_image_without_either_optional_api_returns_empty_for_driver_fallback(self):
  with patch.dict(sys.modules,modules()):self.assertEqual(codec.image_codec_name(7),'')
if __name__=='__main__':unittest.main()
