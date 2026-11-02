#!/usr/bin/env python3
"""Exercise the copied ATV painters on actual native PLi list state/geometry.

Captures the real MultiContent draw commands, not a replacement mock renderer.
Physical C++/TV rendering still requires receiver confirmation.
"""
import argparse,ast,base64,hashlib,importlib.util,json,sys,time,unittest
from pathlib import Path
from types import ModuleType,SimpleNamespace as NS
from unittest.mock import patch
P=argparse.ArgumentParser();P.add_argument('--upstream',type=Path,required=True);P.add_argument('--package-root',type=Path);args,rest=P.parse_known_args()
ROOT=Path(__file__).resolve().parents[1];PAYLOAD=args.package_root or ROOT/'source/package-root';RUNTIME=PAYLOAD/'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec=importlib.util.spec_from_file_location('atv_paint',RUNTIME/'warderAtvEpgPaint.py');paint=importlib.util.module_from_spec(spec);spec.loader.exec_module(paint)
RECORD=json.loads((ROOT/'design/openpli-graph-epg/atv-assets.json').read_text())
NATIVE=args.upstream/'Plugins/Extensions/GraphMultiEPG/GraphMultiEpg.py';TREE=ast.parse(NATIVE.read_text())
class Size:
 def __init__(self,w,h):self.w,self.h=int(w),int(h)
 def width(self):return self.w
 def height(self):return self.h
class Rect:
 def __init__(self,x,y,w,h):self.x,self.y,self.w,self.h=x,y,w,h
 def left(self):return self.x
 def top(self):return self.y
 def width(self):return self.w
 def height(self):return self.h
class Content:
 def __init__(self):self.height=33;self.width=1845;self.rows=[]
 def setBuildFunc(self,fn):self.builder=fn
 def setSelectableFunc(self,fn):pass
 def setFont(self,*args):pass
 def setSelectionClip(self,*args):pass
 def setItemHeight(self,h):self.height=h
 def getItemSize(self):return Size(self.width,self.height)
 def getCurrentSelectionIndex(self):return 0
 def setList(self,rows):self.rows=rows
class Widget:
 def __init__(self,w=1845,h=495):self.sz=Size(w,h)
 def size(self):return self.sz
 def position(self):return NS(x=lambda:15)
class GUI:
 def __init__(self):self.instance=Widget();self.skinAttributes=[]
def command(kind):return lambda **kw:dict(kind=kind,**kw)
def module(name,**kw):m=ModuleType(name);m.__dict__.update(kw);return m
V=lambda value:NS(value=value,getValue=lambda:value)
def environment():
 skin=PAYLOAD/'usr/share/enigma2/hd_glass17'
 def resolve(scope,path):return str(skin/path)
 def load(path=None,cached=False):return Path(path).name if path and Path(path).is_file() else None
 env={'GUIComponent':GUI,'gFont':lambda *a:a,'applySkinFactor':lambda n:n,'eListboxPythonMultiContent':Content,'eEPGCache':NS(getInstance=lambda:None),'eListbox':object(),'LoadPixmap':load,'resolveFilename':resolve,'SCOPE_CURRENT_SKIN':0,'time':lambda:1050,'config':NS(misc=NS(graph_mepg=NS(ev_fontsize=V(0),show_record_clocks=V(True))))}
 cls=next(n for n in TREE.body if isinstance(n,ast.ClassDef) and n.name=='EPGList');exec(compile(ast.Module(body=[cls],type_ignores=[]),str(NATIVE),'exec'),env)
 flags={'RT_HALIGN_LEFT':1,'RT_HALIGN_CENTER':2,'RT_HALIGN_RIGHT':4,'RT_VALIGN_CENTER':8,'BT_SCALE':16,'BT_KEEP_ASPECT_RATIO':32}
 mods={'enigma':module('enigma',**flags,gFont=lambda *a:a,eSize=Size),'Components.EpgList':module('Components.EpgList',Rect=Rect),'Components.MultiContent':module('Components.MultiContent',MultiContentEntryText=command('text'),MultiContentEntryPixmapAlphaTest=command('pixmap'),MultiContentEntryPixmapAlphaBlend=command('blend')),'Components.Renderer.Picon':module('Components.Renderer.Picon',getPiconName=lambda s:'picon.png'),'Tools.LoadPixmap':module('Tools.LoadPixmap',LoadPixmap=load),'Tools.Alternatives':module('Tools.Alternatives',CompareWithAlternatives=lambda a,b:a==b),'Tools.TextBoundary':module('Tools.TextBoundary',getTextBoundarySize=lambda *a:Size(60,30)),'Tools.Directories':module('Tools.Directories',resolveFilename=resolve,SCOPE_CURRENT_SKIN=0)}
 listing=env['EPGList'](timer=NS(isInTimer=lambda *a:None));listing.listWidth=1845;listing.listHeight=495;listing.time_base=1000;listing.time_epoch=180;listing.offs=0;listing.cur_service=('station','Station',[],None,None);listing.showPicon=True;listing.showChannelNumber=False
 listing.list=[listing.cur_service];listing.select_rect=Rect(60,0,200,33)
 with patch.dict(sys.modules,mods):painter=paint.install_painter(listing);timeline=NS();timeline_builder=paint.install_timeline(timeline,painter)
 listing.recalcEntrySize();painter.api.time=lambda:1050;painter.paint=paint.make_graph_builder(painter.api).__get__(painter,type(painter));listing.l.setBuildFunc(painter.paint)
 return listing,painter,timeline,timeline_builder
class Tests(unittest.TestCase):
 def test_copied_atv_painter_body_is_unchanged(self):
  tree=ast.parse((RUNTIME/'warderAtvEpgPaint.py').read_text());fn=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='buildGraphEntry')
  self.assertEqual(hashlib.sha256(ast.dump(fn,include_attributes=False).encode()).hexdigest(),RECORD['painter_ast_sha256'])
 def test_all_pinned_pngs_are_shipped_and_original(self):
  for name,item in RECORD['assets'].items():
   data=(PAYLOAD/'usr/share/enigma2/hd_glass17/epg/atv'/name).read_bytes();self.assertEqual(hashlib.sha256(data).hexdigest(),item['sha256']);self.assertEqual(data,base64.b64decode(item['base64']));self.assertTrue(data.startswith(b'\x89PNG\r\n\x1a\n'))
 def test_future_current_selected_recording_and_zap_use_original_textures(self):
  listing,painter,_,_=environment();events=[(1,'Now',1000,100),(2,'Future',1100,300)]
  for selected in (True,False):
   listing.cur_service=('station' if selected else 'other','Station',[],None,None)
   commands=listing.l.builder('station','Station',events,'',None)
   pngs=[c.get('png') for c in commands[1:] if c['kind']=='pixmap']
   self.assertIn('OtherEvent.png',pngs);self.assertIn('SelectedCurrentEvent.png' if selected else 'CurrentEvent.png',pngs)
   self.assertIn('BorderLeft.png',pngs);self.assertIn('SelectedBorderRight.png' if selected else 'BorderRight.png',pngs)
   text=next(c for c in commands[1:] if c.get('text')=='Future');self.assertIsNone(text['backcolor']);self.assertEqual(text['pos'][1],1)
  listing.timer.isInTimer=lambda *a:(100,[2],0);commands=listing.l.builder('station','Station',events,'',None);self.assertTrue(any(c.get('png')=='RecordEvent.png' for c in commands[1:]));listing.timer.isInTimer=lambda *a:(100,[7],0);commands=listing.l.builder('station','Station',events,'',None);self.assertTrue(any(c.get('png')=='ZapEvent.png' for c in commands[1:]))
 def test_native_selection_geometry_matches_atv_picon_width_at_all_scales(self):
  listing,painter,_,_=environment()
  for width,height in ((1230,22),(1845,33),(2460,44),(3690,66)):
   listing.listWidth=listing.l.width=width;listing.l.height=height;listing.recalcEntrySize();self.assertEqual(listing.service_rect.w,round(60*width/1845));self.assertEqual(listing.event_rect.w+listing.service_rect.w,width);self.assertEqual(listing.picon_size.height(),height-2)
 def test_atv_timeline_uses_gradient_and_three_hour_span(self):
  listing,painter,timeline,build=environment();timeline.l=Content();timeline.listHeight=36;timeline.time_base=timeline.time_epoch=0
  class Pix:
   def __init__(self):self.position=(75,423);self.instance=Widget(28);self.visible=False
   def setPosition(self,x,y):self.position=(x,y)
  listing.getEventRect=lambda:Rect(75,0,1785,33);listing.getServiceRect=lambda:Rect(15,0,60,33)
  now=Pix();lines=[Pix() for _ in range(6)];build(listing,now,lines,True);commands=timeline.l.rows[0]
  self.assertTrue(any(c.get('png')=='TimeLineTime.png' for c in commands[1:]));times=[c['text'] for c in commands[1:] if c.get('text','').count(':')==1];self.assertEqual(len(times),6);self.assertTrue(all(c['size'][1]==36 for c in commands[1:]));self.assertEqual(listing.time_epoch,180)
if __name__=='__main__':unittest.main(argv=[sys.argv[0]]+rest)
