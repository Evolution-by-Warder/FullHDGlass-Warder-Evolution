import hashlib, importlib.util, io, os, shutil, struct, tempfile, unittest, zipfile, zlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/warderCanonicalPicons.py'
s=importlib.util.spec_from_file_location('canonical',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def png(c):
 # Generate genuine RGBA PNG fixtures without a network-installed Pillow dependency.
 rgba={'red':b'\xff\x00\x00\xff','blue':b'\x00\x00\xff\xff'}[c]
 def chunk(kind,data):
  return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
 return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',220,132,8,6,0,0,0))+chunk(b'IDAT',zlib.compress((b'\x00'+rgba*220)*132))+chunk(b'IEND',b'')
def entry(files, url, delivery='canonical-220x132-v1'):
 b=io.BytesIO()
 with zipfile.ZipFile(b,'w') as z:
  for n,d in files.items():z.writestr('piconProv/'+n,d)
 raw=b.getvalue();return dict(url=url,delivery=delivery,root='piconProv',filename='piconProv.zip',publication_source_id='fullhd-production',resolution=[220,132],sha256=hashlib.sha256(raw).hexdigest(),size=len(raw),png_count=len(files)),raw
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name);self.dest=self.base/'piconProv';self.dest.mkdir()
  self.raw={};self.copies=0;self.a=png('red');self.b=png('blue')
  x,r=entry({'a.png':self.a},m._PROVIDER_ROOT+'white/piconProv.zip');self.raw[x['url']]=r
  y,r=entry({'b.png':self.b},m._PROVIDER_ROOT+'white/extension-01/piconProv.zip','canonical-220x132-v2');self.raw[y['url']]=r
  self.assets={'piconProv-w':x,'piconProv-w-v2':dict(delivery='canonical-220x132-v2',resolution=[220,132],root='piconProv',base_asset_id='piconProv-w',base_sha256=x['sha256'],extensions=[y],png_count=2,unpacked_size=len(self.a)+len(self.b))}
  outer=self
  class Screen:
   zzz='original'
   def _warderAuxiliaryDestination(self,root):return str(outer.dest)
   def _warderFetchAuxiliaryArchive(self,asset,path,progress=None):
    raw=outer.raw[asset['url']];assert hashlib.sha256(raw).hexdigest()==asset['sha256'];Path(path).write_bytes(raw)
    if progress:progress(len(raw),len(raw))
   def cprmFiles(self,root):
    outer.copies+=1
    files=list((Path(self.zzz)/root).glob('*.png'))
    for f in files:shutil.copyfile(f,outer.dest/f.name)
    return len(files),len(files)
   def _warderFilesMatch(self,a,b):return Path(a).read_bytes()==Path(b).read_bytes()
  self.screen=Screen()
 def run_install(self):
  return m.install(self.screen,'aux-prov','white',lambda:('',self.assets),lambda x:x)
 def test_success(self):
  self.assertIn('2/2',self.run_install());self.assertEqual((self.dest/'a.png').read_bytes(),self.a);self.assertEqual((self.dest/'b.png').read_bytes(),self.b);self.assertEqual(self.screen.zzz,'original');self.assertEqual(self.copies,1);self.assertEqual(list(self.base.glob('.warder-provider-*')),[])
 def test_old_base_unchanged(self):
  self.assertEqual(self.assets['piconProv-w']['delivery'],'canonical-220x132-v1');self.assertLess(self.assets['piconProv-w']['size'],32*1024*1024)
 def test_invalid_base(self):
  self.assets['piconProv-w-v2']['base_sha256']='0'*64
  with self.assertRaises(ValueError):self.run_install()
  self.assertEqual(self.copies,0)
 def test_duplicate(self):
  y,r=entry({'A.png':self.b},m._PROVIDER_ROOT+'white/extension-01/piconProv.zip','canonical-220x132-v2');self.raw[y['url']]=r;self.assets['piconProv-w-v2']['extensions']=[y]
  with self.assertRaises(ValueError):self.run_install()
  self.assertEqual(self.copies,0);self.assertEqual(list(self.dest.iterdir()),[]);self.assertEqual(list(self.base.glob('.warder-provider-*')),[])
 def test_bad_url(self):
  self.assets['piconProv-w-v2']['extensions'][0]['url']='https://example.com/piconProv.zip'
  with self.assertRaises(ValueError):self.run_install()
  self.assertEqual(self.copies,0)
 def test_large_part(self):
  self.assets['piconProv-w-v2']['extensions'][0]['size']=32*1024*1024+1
  with self.assertRaises(ValueError):self.run_install()
  self.assertEqual(self.copies,0)
 def test_low_space(self):
  with patch.object(m.os,'statvfs',return_value=SimpleNamespace(f_bavail=1,f_frsize=4096)):
   with self.assertRaises(OSError):self.run_install()
  self.assertEqual(self.copies,0)
 def test_wrong_expansion(self):
  self.assets['piconProv-w-v2']['unpacked_size']=1
  with self.assertRaises(ValueError):self.run_install()
  self.assertEqual(self.copies,0)
if __name__=='__main__':unittest.main()
