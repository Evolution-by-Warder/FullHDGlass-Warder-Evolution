#!/usr/bin/env python3
"""Run native OpenPLi graphical controller/action maps with fake C++/EPG data."""
import argparse,ast,importlib.util,json,sys,time,unittest
from pathlib import Path
from types import SimpleNamespace as NS, ModuleType
from unittest.mock import patch
import xml.etree.ElementTree as ET
P=argparse.ArgumentParser();P.add_argument('--upstream',type=Path,required=True);P.add_argument('--package-root',type=Path);args,rest=P.parse_known_args()
ROOT=Path(__file__).resolve().parents[1];PAYLOAD=args.package_root or ROOT/'source/package-root';RUNTIME=PAYLOAD/'usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec=importlib.util.spec_from_file_location('pli_graph_compat',RUNTIME/'warderOpenPliEpg.py');compat=importlib.util.module_from_spec(spec);spec.loader.exec_module(compat)
NATIVE=args.upstream/'Plugins/Extensions/GraphMultiEPG/GraphMultiEpg.py';TREE=ast.parse(NATIVE.read_text())
def node(name):return next(n for n in TREE.body if isinstance(n,ast.ClassDef) and n.name==name)
def method(cls,name,scope):
 n=next(n for n in node(cls).body if isinstance(n,ast.FunctionDef) and n.name==name);env=dict(scope);exec(compile(ast.Module(body=[n],type_ignores=[]),str(NATIVE),'exec'),env);return env[name]
class Text:
 def __init__(self,value=''):self.text=value
 def setText(self,value):self.text=value
 def getText(self):return self.text
class Size:
 def __init__(self,w,h):assert type(w) is int and type(h) is int;self.w,self.h=w,h
 def width(self):return self.w
 def height(self):return self.h
class Rect:
 def __init__(self,left,width):self.x,self.w=left,width
 def left(self):return self.x
 def width(self):return self.w
class Widget:
 def __init__(self,w=1,h=495):self.sz=Size(w,h)
 def size(self):return self.sz
 def resize(self,size):self.sz=size
class Pixmap:
 def __init__(self):self.position=(75,423);self.instance=Widget(28);self.visible=True
 def setPosition(self,x,y):self.position=(x,y)
class Content:
 def __init__(self):self.height=25;self.rows=[]
 def setItemHeight(self,h):self.height=h
 def getItemSize(self):return Size(1845,self.height)
 def setList(self,rows):self.rows=rows
 def invalidate(self):pass
class Timer:
 def __init__(self):self.callback=[];self.started=[]
 def start(self,*a):self.started.append(a)
class Screen(dict):
 def __init__(self,session):super().__init__();self.session=session;self.onLayoutFinish=[];self.onClose=[];self.helpList=[];self.shown=True;self.skinName=type(self).__name__;self.title='';self.closed=[]
 def setTitle(self,title,*a,**kw):self.title=title
 def show(self):self.shown=True
 def hide(self):self.shown=False
 def close(self,*a):self.closed.append(a)
class Help:
 def __init__(self):pass
class Session:
 def __init__(self):self.opens=[];self.fail=False;self.nav=NS(RecordTimer=NS(getAllTimersList=lambda:[]),getCurrentlyPlayingServiceOrGroup=lambda:REF)
 def openWithCallback(self,callback,screen,*args,**kwargs):
  if self.fail:raise RuntimeError('native GUI failure')
  self.opens.append((callback,screen,args,kwargs));return self.opens[-1]
 def open(self,screen,*args,**kwargs):self.opens.append((None,screen,args,kwargs));return self.opens[-1]
REF=NS(toString=lambda:'1:0:1:A:B:C:0:0:0:0:');SERVICE=NS(ref=REF,getServiceName=lambda:'Selected station');EVENT=NS(getEventName=lambda:'Selected future programme',getEventId=lambda:42,getBeginTime=lambda:2000000000,getDuration=lambda:3600)
class Listing:
 def __init__(self,selChangedCB=None,**kwargs):self.current=(EVENT,SERVICE);self.onSel=selChangedCB;self.l=Content();self.instance=Widget(1845);self.listHeight=495;self.listWidth=1845;self.entryFontSize=27;self.calls=[];self.time_epoch=kwargs.get("time_epoch",120);self.base=2000000000
 def getCurrent(self):return self.current
 def setItemsPerPage(self):self.l.setItemHeight(82)
 def recalcEntrySize(self):pass
 def setShowServiceMode(self,mode):self.calls.append(('service-mode',mode))
 def fillMultiEPG(self,*args):self.calls.append(('fill',args));self.onSel()
 def moveToService(self,ref):self.calls.append(('select',ref))
 def setCurrentlyPlaying(self,ref):self.calls.append(('playing',ref))
 def getServiceRect(self):return Rect(15,64)
 def getEventRect(self):return Rect(79,1781)
 def getTimeEpoch(self):return self.time_epoch
 def getTimeBase(self):return self.base
 def resetOffset(self):pass
 def setEpoch(self,e):self.time_epoch=e
 def moveTo(self,*a):pass
class Timeline:
 def __init__(self):self.position=(15,387);self.instance=Widget(1845,36);self.l=Content();self.time_base=0;self.time_epoch=0;self.foreColor=1;self.backColor=0;self.datefmt='%d-%m'
 def applySkin(self,*args):self.l.setItemHeight(25);return True
 def setDateFormat(self,value):self.datefmt='%d-%m'
class Value:
 def __init__(self,value):self.value=value
 def getValue(self):return self.value

def setup(active=True,listscreen=False):
 cfg=NS(skin=NS(primary_skin=Value('hd_glass17/skin.xml' if active else 'Other/skin.xml')),misc=NS(graph_mepg=NS(roundTo=Value('900'),prev_time_period=Value(120),overjump=Value(True),ev_fontsize=Value(0),servicetitle_mode=Value('picon+servicename'),zap_blind_bouquets=Value(False),center_timeline=Value(False),show_timelines=Value('all'),OKButton=Value('zap'),prev_time=Value([20,0]),save=lambda:None)))
 gui=NS(getInstance=lambda:NS(bindAction=lambda *a:None,unbindAction=lambda *a:None))
 action_scope={'eActionMap':gui,'queryKeyBinding':lambda *a:True}
 action_tree=ast.parse((args.upstream/'Components/ActionMap.py').read_text());exec(compile(ast.Module(body=[n for n in action_tree.body if isinstance(n,ast.ClassDef) and n.name in ('ActionMap','HelpableActionMap')],type_ignores=[]),'native-actionmaps','exec'),action_scope)
 cfg.recording=NS(timer_default_type=Value('record'))
 scope={'Screen':Screen,'HelpableScreen':Help,'Button':Text,'StaticText':Text,'TimelineText':Timeline,'Pixmap':Pixmap,'ServiceEvent':lambda:NS(newService=lambda value:None),'Event':lambda:NS(newEvent=lambda value:None),'EPGList':Listing,'HelpableActionMap':action_scope['HelpableActionMap'],'config':cfg,'time':lambda:2000000100,'localtime':time.localtime,'listscreen':listscreen,'MAX_TIMELINES':6,'_':lambda s:s,'eTimer':Timer,'FallbackTimerList':lambda *a:None,'Screens':NS(InfoBar=NS(InfoBar=NS(instance=NS(servicelist=NS(getCurrentSelection=lambda:REF))))),'TimeDateInput':object(),'createRecordTimerEntry':lambda *a:NS(event=a[-1] if a else None),'TimerEntry':object(),'RecordTimerEntry':lambda service,*a,**kw:NS(service_ref=service,event=a[0]),'preferredTimerPath':lambda:'/media/hdd/movie','parseEvent':lambda event:(event,)}
 exec(compile(ast.Module(body=[node('GraphMultiEPG')],type_ignores=[]),str(NATIVE),'exec'),scope);native=scope['GraphMultiEPG']
 timeline_scope=dict(scope,MultiContentEntryText=lambda **kw:kw,RT_HALIGN_LEFT=1,RT_HALIGN_CENTER=2,RT_VALIGN_CENTER=4,strftime=time.strftime)
 Timeline.setEntries=method('TimelineText','setEntries',timeline_scope)
 class InfoBar:
  def __init__(self):self.session=Session();self.servicelist=NS();self.calls=[]
  def openMultiServiceEPG(self,withCallback=True):self.calls.append(withCallback);return 'native-multi'
 plugin=NS(GraphMultiEPG=native)
 def launch(session,servicelist=None,**kwargs):return plugin.GraphMultiEPG(session,[SERVICE],lambda *a,**kw:None)
 plugin.main=launch;errors=[];searches=[];program=object()
 compat.install(NS(GraphMultiEPG=native),plugin,InfoBar,cfg,Text,action_scope['HelpableActionMap'],Size,program,lambda s:'translated:'+s,search=lambda session,event,tr:searches.append(event),report_error=errors.append,paint_installer=lambda listing:None)
 return NS(config=cfg,plugin=plugin,native=native,InfoBar=InfoBar,program=program,errors=errors,searches=searches)
class Tests(unittest.TestCase):
 def test_native_multi_entry_opens_owned_layout_and_keeps_selected_event(self):
  a=setup();bar=a.InfoBar();screen=bar.openMultiServiceEPG();self.assertIn('FullHDGlassOpenPLiGraphEPG',screen.skinName)
  before=screen['list'].getCurrent();screen['warderEpgActions'].action('GMEPGSelectActions','red');opened=screen.session.opens[-1]
  self.assertIs(opened[1],a.program);self.assertEqual(opened[2],before);opened[0]();self.assertEqual(screen['list'].getCurrent(),before)
 def test_both_native_modes_have_same_owned_layout_and_colour_captions(self):
  for mode in (False,True):
   a=setup(listscreen=mode);s=a.plugin.main(Session());s.onSelectionChanged();self.assertIn('FullHDGlassOpenPLiGraphEPG',s.skinName)
   for colour in ('red','yellow','blue'):self.assertTrue(s['warder_key_'+colour].text.startswith('translated:'))
   self.assertEqual(s['warder_key_green'].text,'Add timer');s.onSelectionChanged();self.assertIn('PROGRAM INFO',s['warder_key_red'].text)
 def test_red_does_not_replace_native_zap_or_ok_actions(self):
  a=setup();s=a.plugin.main(Session());self.assertIs(type(s).zapTo,a.native.zapTo);self.assertIs(type(s).eventSelected,a.native.eventSelected)
  self.assertEqual(s['gmepgactions'].actions['red'].__func__,a.native.zapTo)
  self.assertEqual(s['warderEpgActions'].prio,-2)
 def test_cpp_dispatch_receives_consumed_integer_and_never_native_red_zap(self):
  a=setup();s=a.plugin.main(Session());s.onSelectionChanged()
  for colour in ('red','red','blue'):
   result=s['warderEpgActions'].action('GMEPGSelectActions',colour)
   self.assertIs(type(result),int);self.assertNotEqual(result,0)
  self.assertEqual(len(s.session.opens),1);self.assertEqual(s.closed,[])
  s.warderProgramInfoClosed();s['list'].current=(None,SERVICE)
  self.assertEqual(s['warderEpgActions'].action('GMEPGSelectActions','red'),1)
 def test_help_lists_only_the_actual_owned_short_colour_actions(self):
  a=setup();s=a.plugin.main(Session())
  for colour in ('red','yellow','blue'):
   entries=[(owner,entry) for owner,context,items in s.helpList for entry in items if context=='GMEPGSelectActions' and entry[0]==colour]
   self.assertEqual(len(entries),1);self.assertIs(entries[0][0],s['warderEpgActions'])
 def test_program_info_lock_cancel_empty_event_and_open_failure(self):
  a=setup();s=a.plugin.main(Session());s.warderProgramInfo();s.warderProgramInfo();self.assertEqual(len(s.session.opens),1);s.session.opens[-1][0]();s.warderProgramInfo();self.assertEqual(len(s.session.opens),2)
  s.warderProgramInfoClosed();s.session.fail=True;s.warderProgramInfo();self.assertFalse(s._warderProgramInfoOpen);self.assertEqual(len(a.errors),1)
  s['list'].current=(None,SERVICE);s.session.fail=False;s.warderProgramInfo();self.assertEqual(len(s.session.opens),2)
 def test_detail_colour_callbacks_reuse_native_timer_date_and_selected_search(self):
  a=setup();s=a.plugin.main(Session());calls=[]
  s.timerAdd=lambda:calls.append('timer');s.enterDateTime=lambda:calls.append('date')
  for colour in ('green','yellow','blue'):s.warderProgramInfoClosed(colour)
  self.assertEqual(calls,['timer','date']);self.assertEqual(a.searches,[EVENT])
  s['warderEpgActions'].action('GMEPGSelectActions','blue');self.assertEqual(a.searches,[EVENT,EVENT])
 def test_green_from_detail_opens_native_timer_editor_for_selected_programme(self):
  a=setup();s=a.plugin.main(Session());s.warderProgramInfo();s.session.opens[-1][0]('green');opened=s.session.opens[-1]
  self.assertIs(opened[2][0].service_ref,SERVICE);self.assertIs(opened[2][0].event,EVENT);self.assertTrue(opened[3]['newEntry'])
 def test_optional_search_plugin_receives_selected_title_and_empty_event_is_safe(self):
  session=Session();module=ModuleType('Plugins.Extensions.EPGSearch.EPGSearch');module.EPGSearch=object()
  with patch.dict(sys.modules,{'Plugins.Extensions.EPGSearch.EPGSearch':module}):compat.open_search(session,EVENT,lambda s:s)
  self.assertEqual(session.opens[-1][2],('Selected future programme',False));self.assertIs(session.opens[-1][1],module.EPGSearch)
  before=len(session.opens);compat.open_search(session,None,lambda s:s);self.assertEqual(len(session.opens),before)
 def test_missing_search_plugin_opens_only_information(self):
  import builtins
  original=builtins.__import__;box=ModuleType('Screens.MessageBox');box.MessageBox=NS(TYPE_INFO=0)
  def importing(name,*a,**kw):
   if name=='Plugins.Extensions.EPGSearch.EPGSearch':raise ImportError('not installed')
   return original(name,*a,**kw)
  session=Session()
  with patch.dict(sys.modules,{'Screens.MessageBox':box}),patch('builtins.__import__',side_effect=importing):compat.open_search(session,EVENT,lambda s:s)
  self.assertIs(session.opens[-1][1],box.MessageBox);self.assertIn('not installed',session.opens[-1][2][0])
 def test_other_skins_and_native_nested_callback_entry_unchanged(self):
  a=setup(False);bar=a.InfoBar();self.assertEqual(bar.openMultiServiceEPG(),'native-multi');self.assertIs(type(a.plugin.main(Session())),a.native)
  a.config.skin.primary_skin.value='hd_glass17/skin.xml';self.assertEqual(bar.openMultiServiceEPG(False),'native-multi')
 def test_picon_mode_is_per_instance_and_native_config_is_not_overwritten(self):
  a=setup();s=a.plugin.main(Session());s['list'].setShowServiceMode('picon+servicename');self.assertEqual(s['list'].calls[-1],('service-mode','picon'));self.assertEqual(a.config.misc.graph_mepg.servicetitle_mode.value,'picon+servicename')
 def test_epoch_changes_are_owned_and_do_not_overwrite_native_settings(self):
  a=setup();s=a.plugin.main(Session());self.assertEqual(s['list'].time_epoch,180);s.updEpoch(240);self.assertEqual(s['list'].time_epoch,240);self.assertEqual(a.config.misc.graph_mepg.prev_time_period.value,120)
 def test_complete_rows_at_hd_fhd_wqhd_uhd_and_large_fonts(self):
  for factor in (2/3,1,4/3,2):
   for font_offset in (0,12):
    a=setup();s=a.plugin.main(Session());listing=s['list'];listing.listHeight=round(495*factor);listing.listWidth=round(1845*factor);listing.entryFontSize=round(27*factor);a.config.misc.graph_mepg.ev_fontsize.value=font_offset;listing.setItemsPerPage();height=listing.instance.size().height();self.assertEqual(height%listing.l.height,0);self.assertLessEqual(height,listing.listHeight);self.assertGreaterEqual(listing.l.height,listing.entryFontSize+font_offset+4)
 def test_native_timeline_uses_complete_header_and_marker_does_not_drift(self):
  a=setup();s=a.plugin.main(Session());timeline=s['timeline_text'];timeline.applySkin(None,s);self.assertEqual(timeline.l.height,36)
  for force in (True,False,True,False):
   s.moveTimeLines(force);self.assertEqual(s['timeline0'].position[0],79);self.assertEqual(timeline.l.rows[0][1]['size'][1],36)
 def test_xml_matches_openatv_geometry_and_has_all_native_timeline_widgets(self):
  skin=ET.parse(PAYLOAD/'usr/share/enigma2/hd_glass17/skin.xml').getroot();own=skin.find("screen[@name='FullHDGlassOpenPLiGraphEPG']");atv=skin.find("screen[@name='GraphicalEPGPIG']");self.assertEqual(own.attrib,{**atv.attrib,'name':'FullHDGlassOpenPLiGraphEPG'})
  for source in ('Event','session.VideoPicture','warder_key_red','warder_key_green','warder_key_yellow','warder_key_blue'):
   original=atv.find("widget[@source='%s']"%source);target=own.find("widget[@source='%s']"%source);self.assertIsNotNone(target);self.assertEqual(target.get('position'),original.get('position'));self.assertEqual(target.get('size'),original.get('size'))
  for n in range(6):self.assertIsNotNone(own.find("widget[@name='timeline%d']"%n))
 def test_registered_addition_keeps_the_entire_stable_skin_unchanged(self):
  import hashlib
  record=json.loads((ROOT/'design/openpli-graph-epg/layout.json').read_text());text=(PAYLOAD/'usr/share/enigma2/hd_glass17/skin.xml').read_text()
  for item in record['additions']:
   self.assertEqual(text.count(item['inserted_text']),1);text=text.replace(item['inserted_text'],'',1)
  self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),record['stable_skin_sha256'])
  changed=text.replace('FullHDGlass Graphical Guide','unexpected OpenATV change',1)
  self.assertNotEqual(hashlib.sha256(changed.encode()).hexdigest(),record['stable_skin_sha256'])
 def test_registration_and_bootstrap_are_openpli_only(self):
  tree=ast.parse((RUNTIME/'plugin.py').read_text());pli=next(n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=='_WarderOpenPli');self.assertIn('_installWarderOpenPliEpg',ast.unparse(pli));plugins=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='Plugins');self.assertIn('FullHDGlass Multi EPG',ast.unparse(plugins))
if __name__=='__main__':unittest.main(argv=[sys.argv[0]]+rest)
