#!/usr/bin/env python3
"""Framed-preview projection and native decoder/PiP lifecycle regressions."""
import argparse
import ast
from fractions import Fraction
from pathlib import Path
import re
import sys
from types import ModuleType, SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--package-root',type=Path)
args,rest=p.parse_known_args()
ROOT=Path(__file__).resolve().parents[1]
PAYLOAD=args.package_root or ROOT/'source/package-root'
RENDERERS=PAYLOAD/'usr/lib/enigma2/python/Components/Renderer'
FRAMES={'hd_glass17/frame/Frame.png','hd_glass17/menu/pig_frame.png','hd_glass17/menu/pig_frame-all-fs8.png'}
EXPECTED={2,4,9,10,11,15,21,27,28,29,30,31,32,38,41}

class Point:
    def __init__(self,x,y):assert type(x) is int and type(y) is int;self.xy=(x,y)
    def x(self):return self.xy[0]
    def y(self):return self.xy[1]
class Size:
    def __init__(self,w,h):assert type(w) is int and type(h) is int;self.wh=(w,h)
    def width(self):return self.wh[0]
    def height(self):return self.wh[1]
class Video:
    def __init__(self,parent=(0,0)):
        self.pos=Point(94,121);self.sz=Size(600,360);self.parent=parent;self.events=[]
    def position(self):return self.pos
    def getAbsolutePosition(self):return Point(self.parent[0]+self.pos.x(),self.parent[1]+self.pos.y())
    def size(self):return self.sz
    def move(self,p):self.pos=p;self.events.append(('move',p.xy))
    def resize(self,s):self.sz=s;self.events.append(('resize',s.wh))
    def updateVideoPosition(self):self.events.append(('refresh',))
    def restoreFullsize(self):self.events.append(('fullscreen',))
    def setDecoder(self,n):self.events.append(('decoder',n))
    def setFBSize(self,s):self.events.append(('framebuffer',s.wh))
    def show(self):self.events.append(('show',))
    def hide(self):self.events.append(('hide',))
class Renderer:
    def __init__(self):self.instance=Video();self.skinAttributes=[]
    def applySkin(self,*a):return True
    def preWidgetRemove(self,instance):instance.events.append(('remove',))

pip=[]
enigma=ModuleType('enigma');enigma.ePoint=Point;enigma.eSize=Size;enigma.getDesktop=lambda n:SimpleNamespace(size=lambda:Size(1920,1080))
native_tree=ast.parse((args.upstream/'Components/Renderer/Pig.py').read_text())
cls=next(n for n in native_tree.body if isinstance(n,ast.ClassDef) and n.name=='Pig')
ns={'Renderer':Renderer,'eVideoWidget':Video,'getDesktop':enigma.getDesktop,'PipPigMode':lambda value:pip.append(value)}
exec(compile(ast.Module(body=[cls],type_ignores=[]),'native-Pig','exec'),ns)
native=ModuleType('Components.Renderer.Pig');native.Pig=ns['Pig']
# Only GUI bindings are faked. Execute the actual image Pig class and our file.
with patch.dict(sys.modules,{'enigma':enigma,'Components.Renderer.Pig':native}):
    scope={'__name__':'frame_projection'}
    exec(compile((RENDERERS/'WarderFramedPig.py').read_text(),'WarderFramedPig','exec'),scope)

class FramedPigTests(unittest.TestCase):
    def test_projection_tracks_the_osd_viewport_at_all_framebuffer_sizes(self):
        rect=(94,121,600,360);vp=(24,16,672,544)
        for fb in [(720,576),(1280,720),(1920,1080),(2560,1440),(3840,2160)]:
            result=scope['project_rectangle'](rect,fb,vp)
            exact=(Fraction(vp[0]*fb[0]+rect[0]*vp[2],720),Fraction(vp[1]*fb[1]+rect[1]*vp[3],576))
            for actual,wanted in zip(result,exact):self.assertLessEqual(abs(actual-wanted),1)
            right=Fraction(vp[0]*fb[0]+(rect[0]+rect[2])*vp[2],720)
            bottom=Fraction(vp[1]*fb[1]+(rect[1]+rect[3])*vp[3],576)
            self.assertEqual(result[2],right.numerator//right.denominator-exact[0].numerator//exact[0].denominator)
            self.assertEqual(result[3],bottom.numerator//bottom.denominator-exact[1].numerator//exact[1].denominator)
            self.assertTrue(all(type(v) is int for v in result))
            self.assertGreater(result[2],0);self.assertGreater(result[3],0)
    def test_missing_unknown_and_full_viewports_keep_native_geometry(self):
        rect=(94,121,600,360)
        for vp in (None,scope['FULL_VIEWPORT']):self.assertEqual(scope['project_rectangle'](rect,(1920,1080),vp),rect)
        item=scope['WarderFramedPig']();item.instance.getAbsolutePosition=None
        with patch.dict(scope,read_viewport=lambda:(24,16,672,544)):
            item.applySkin(None,None);item.onShow()
            self.assertEqual(item.instance.pos.xy,(94,121))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.assertIsNone(scope['read_viewport'](root))
            for values in [('00000018','00000010','000002a0','00000220'),('invalid','0','0','0'),('0','0','00000780','00000438')]:
                for n,v in zip(('left','top','width','height'),values):(root/('dst_'+n)).write_text(v)
                expected=(24,16,672,544) if values[0]=='00000018' else None
                self.assertEqual(scope['read_viewport'](root),expected)
    def test_native_show_hide_and_decoder_handling_remain_with_the_image(self):
        pip.clear();item=scope['WarderFramedPig']();item.instance=Video((60,30))
        item.postWidgetCreate(item.instance)
        self.assertIn(('decoder',0),item.instance.events)
        with patch.dict(scope,read_viewport=lambda:(24,16,672,544)):
            original=native.Pig();original.applySkin(None,None);original.onShow()
            self.assertEqual(original.instance.pos.xy,(94,121))
            pip.clear()
            item.applySkin(None,None)
            x,y,w,h=scope['project_rectangle']((154,151,600,360),(1920,1080),(24,16,672,544))
            expected=((x-60,y-30),(w,h))
            self.assertEqual((item.instance.pos.xy,item.instance.sz.wh),expected)
            self.assertNotEqual(expected[0],(94,121))
            for _ in range(3):
                item.onShow();self.assertEqual((item.instance.pos.xy,item.instance.sz.wh),expected)
                item.onHide()
            self.assertEqual(pip,[True,False]*3)
            self.assertEqual(item.Position.xy,(94,121));self.assertEqual(item.Size.wh,(600,360))
            event='fullscreen' if 'restoreFullsize' in ast.unparse(next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='onHide')) else 'remove'
            self.assertEqual(sum(e[0]==event for e in item.instance.events),3)
            with patch.dict(scope,read_viewport=lambda:None):
                item.onShow();self.assertEqual(item.instance.pos.xy,(94,121));self.assertEqual(item.instance.sz.wh,(600,360))
    def test_legacy_miniptv_keeps_activation_and_pip_cleanup(self):
        class Timer:
            def __init__(self):self.callback=[];self.timeout=SimpleNamespace(connect=lambda callback:None);self.starts=[]
            def stop(self):pass
            def start(self,*args):self.starts.append(args)
        tree=ast.parse((RENDERERS/'g17MiniTV.py').read_text())
        mini_cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='g17MiniTV')
        env={'Renderer':Renderer,'eVideoWidget':Video,'eTimer':Timer,'getDesktop':enigma.getDesktop,'SystemInfo':{'NumVideoDecoders':2}}
        exec(compile(ast.Module(body=[mini_cls],type_ignores=[]),'shipped-g17MiniTV','exec'),env)
        module=ModuleType('Components.Renderer.g17MiniTV');module.g17MiniTV=env['g17MiniTV']
        frame=ModuleType('Components.Renderer.WarderFramedPig');frame.FramedVideoMixin=scope['FramedVideoMixin']
        infobar=ModuleType('Screens.InfoBar');infobar.InfoBar=SimpleNamespace(instance=SimpleNamespace(session=SimpleNamespace(pipshown=False)))
        wrapped={}
        with patch.dict(sys.modules,{'Components.Renderer.g17MiniTV':module,'Components.Renderer.WarderFramedPig':frame,'Screens.InfoBar':infobar}):
            exec(compile((RENDERERS/'WarderFramedMiniTV.py').read_text(),'WarderFramedMiniTV','exec'),wrapped)
            item=wrapped['WarderFramedMiniTV']();closed=[]
            item.source=SimpleNamespace(shown=False,setPiPService=lambda:True,closePiPService=lambda:closed.append(True))
            with patch.dict(scope,read_viewport=lambda:(24,16,672,544)):
                item.applySkin(None,None);item.onShow();rectangle=(item.instance.pos.xy,item.instance.sz.wh)
                self.assertTrue(item.source.shown);self.assertIn((500,),item.timer.starts)
                item.activatePiP();self.assertEqual((item.instance.pos.xy,item.instance.sz.wh),rectangle)
                self.assertIn(('show',),item.instance.events)
                item.onHide();self.assertFalse(item.source.shown);self.assertEqual(closed,[True])

    def test_all_framed_channel_types_keep_their_frame_and_radio_geometry(self):
        catalog=PAYLOAD/'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/hdg17Screens.xml'
        found=set()
        for raw in re.findall(r'<screen\b.*?</screen>',catalog.read_text(),re.S):
            element=ET.fromstring(raw);m=re.fullmatch(r'ChannelSelection-(\d+)',element.get('name',''))
            if not m or not any(n.get('pixmap') in FRAMES for n in element):continue
            found.add(int(m[1]));widgets=[n for n in element.findall('widget') if n.get('render') in ('WarderFramedPig','WarderFramedMiniTV')]
            self.assertEqual(len(widgets),1,m[1])
            self.assertFalse(any(n.get('render') in ('Pig','g17MiniTV') for n in element.findall('widget')))
            if m[1]!='27':
                radio=next(n for n in element.findall('widget') if n.get('pixmap')=='hd_glass17/warder-radio-background.jpg')
                self.assertEqual(radio.get('position'),widgets[0].get('position'));self.assertEqual(radio.get('size'),widgets[0].get('size'))
        self.assertEqual(found,EXPECTED)
    def test_no_global_renderer_or_proc_writes_are_introduced(self):
        source=(RENDERERS/'WarderFramedPig.py').read_text()
        self.assertNotIn('write_text',source);self.assertNotIn('writeProc',source)
        self.assertNotIn('onHide',scope['FramedVideoMixin'].__dict__)
        self.assertIs(scope['WarderFramedPig'].__mro__[2],native.Pig)

if __name__=='__main__':unittest.main(argv=[sys.argv[0]]+rest)
