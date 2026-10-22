#!/usr/bin/env python3
"""Exercise the real receiver queue for two positions in every supplied size/style."""
import ast, hashlib, importlib.util, io, json, os, shutil, stat, struct, tempfile, zipfile, zlib
from pathlib import Path
from urllib.request import Request
R=Path(__file__).resolve().parents[1]; P=R/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec=importlib.util.spec_from_file_location('sync',P/'warderPiconSync.py');sync=importlib.util.module_from_spec(spec);spec.loader.exec_module(sync)
pub=sync.runtime_publication()
def sha(b):return hashlib.sha256(b).hexdigest()
def png(w,h,level):
 def chunk(n,b):return struct.pack('>I',len(b))+n+b+struct.pack('>I',zlib.crc32(n+b)&0xffffffff)
 return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,2,0,0,0))+chunk(b'IDAT',zlib.compress((b'\0'+bytes([level,40,80])*w)*h))+chunk(b'IEND',b'')
class Response(io.BytesIO):
 def __init__(self,data,url):super().__init__(data);self.url=url
 def geturl(self):return self.url
responses={};requests=[]
def open_url(request,timeout):
 requests.append(request);return Response(responses[request.full_url],request.full_url)
names={'_warderRunChannelQueue','_warderLoadChannelManifest','_warderFetchChannelJob','_warderInstallChannelArchive','_warderRemoveStaleChannelPicons'}
scope=dict(warderPiconSync=sync,os=os,shutil=shutil,stat=stat,tempfile=tempfile,zipfile=zipfile,hashlib=hashlib,json=json,Request=Request,urlopen=open_url,_=lambda s:s)
methods=[n for n in ast.walk(ast.parse((P/'plugin.py').read_bytes())) if isinstance(n,ast.FunctionDef) and n.name in names];assert len(methods)==len(names)
for m in methods:exec(compile(ast.Module(body=[m],type_ignores=[]),'receiver','exec'),scope)
Receiver=type('Receiver',(),{n:scope[n] for n in names})
for size in ('50x30','220x132','400x240'):
 for style in ('transparent','white','black'):
  with tempfile.TemporaryDirectory() as temp:
   dest=Path(temp);keep=dest/'1_0_1_1_1_1_C00000_0_0_0.png';keep.write_bytes(b'unrelated existing picon')
   doc=dict(schema=1,generated_from=dict(repository='Evolution-by-Warder/PiconHub-Warder-Evolution',ref='2d5b1ec8d37742825bb5571508c856d919590377'),delivery='direct',packages=[])
   expected={}
   for selector,namespace in [('160E','A00000'),('235E','EB0000')]:
    image=png(*map(int,size.split('x')),80 if selector=='160E' else 160);name='1_0_1_123_1_1_'+namespace+'_0_0_0.png';expected[name]=image
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as z:z.writestr(name,image)
    data=stream.getvalue();filename='routing-'+selector+'-'+size+'-'+style+'.zip';url=pub['package_root']+filename
    doc['packages'].append(dict(selector_id=selector,family='channel-'+style,resolution=size,filename=filename,bytes=len(data),sha256=sha(data),url=url,png_count=1));responses[url]=data
   assert not sync.validate_publication_manifest(doc)
   responses[pub['manifest_url']]=json.dumps(doc).encode()
   prefs=sync.set_task_position_bindings(sync.default_preferences(str(dest)),[sync.task_binding_for_package_selector(s) for s in ('160E','235E')]);prefs.update(resolution=size,style=style,update_mode=sync.UPDATE_MODE_INCREMENTAL,prepared=True)
   receiver=Receiver();receiver.warderPiconPrefs=prefs;receiver.warderChannelQueue=None
   for tick in range(6):
    result=receiver._warderRunChannelQueue()
    if result is not None:break
   assert result.startswith('SUCCESSFUL'),(size,style,result)
   assert keep.read_bytes()==b'unrelated existing picon'
   for n,b in expected.items():assert (dest/n).read_bytes()==b and struct.unpack('>II',b[16:24])==tuple(map(int,size.split('x')))
assert sync.channel_delivery_backend('150x90','black')=='pinned-legacy'
assert sync.selector_id_for_position('80.0e')=='800E'
for label in ('(0.8W) Digi','(0.8W) Telly'):
 binding=sync.task_binding_for_display_label(label);assert binding and 'DIGI_TELLY' in str(binding),binding
assert all(r.get_header('Cache-control')=='no-cache' for r in requests if r.full_url==pub['manifest_url'])
print('PASS: actual receiver installs both selected positions in all nine size/style combinations; destination, PNG dimensions, fresh catalogue and legacy 150x90 preserved')
