"""Reproduce the published EPG integration failure against pinned OpenATV APIs.

This is a controller-interface harness, not a physical Enigma2 receiver test.
Execute the unchanged FullHDGlass EPG patch with the real modern compatibility
metaclass/factory and minimal GUI stand-ins. No image-owned files are modified.
"""
from pathlib import Path
from types import ModuleType,SimpleNamespace
import argparse,ast,hashlib,json,sys,traceback,xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py'
SKIN=ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml'
KEYS=tuple('warder_key_'+c for c in ('red','green','yellow','blue'))

def class_node(source,name):
    return next(n for n in ast.parse(source).body if isinstance(n,ast.ClassDef) and n.name==name)

def patch_nodes():
    nodes=ast.parse(PLUGIN.read_text()).body
    i=next(i for i,n in enumerate(nodes) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='WarderEPGSelection_setTitle' for t in n.targets))
    assert isinstance(nodes[i+1],ast.Try)
    return ast.Module(body=nodes[i:i+2],type_ignores=[])

class Text:
    def __init__(self,text=''):self.text=text
    def setText(self,text):self.text=text

def run_snapshot(before,after,modern):
    class Screen(dict):
        def __init__(self,*args,**kwargs):
            super().__init__();self.skinName='GraphicalEPGPIG';self.activeList='' if modern else 1
        def setTitle(self,title,*args,**kwargs):self.title=title
    module=ModuleType('Screens.EpgSelection')
    if modern:
        # Use upstream's actual metaclass and __new__ factory rather than a
        # lookalike implementation. __init__ wrappers are intentionally not
        # forwarded by EPGSelectionMeta; the real source documents that contract.
        env={'__name__':'Screens.EpgSelection','EPGSelectionBase':Screen,'EPGSelectionSingle':Screen,'EPGSettings':lambda *_:None,'EPG_TYPE_SIMILAR':1}
        nodes=[class_node(after,n) for n in ('EPGStandardButtons','EPGSelectionMeta','EPGSelection')]
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned-openatv-EpgSelection.py','exec'),env)
        class Grid(Screen,env['EPGStandardButtons']):pass
        Grid.__name__='EPGSelectionGrid'
        env['createEPGSelection']=lambda *args,**kwargs:Grid()
        module.EPGSelection=env['EPGSelection'];module.EPGSelectionGrid=Grid
        assert not hasattr(module.EPGSelection,'RefreshColouredKeys')
    else:
        names={n.name for n in class_node(before,'EPGSelection').body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
        required=('RefreshColouredKeys','redButtonPressed','greenButtonPressed','yellowButtonPressed','blueButtonPressed')
        assert set(required)<=names
        class Legacy(Screen):pass
        Legacy.__name__='EPGSelection'
        def native(*args,**kwargs):return None
        for name in required:setattr(Legacy,name,native)
        module.EPGSelection=Legacy
    screens=ModuleType('Screens');screens.EpgSelection=module
    old_modules={name:sys.modules.get(name) for name in ('Screens','Screens.EpgSelection')}
    sys.modules['Screens']=screens;sys.modules['Screens.EpgSelection']=module
    env={'config':SimpleNamespace(skin=SimpleNamespace(primary_skin=SimpleNamespace(value='hd_glass17/skin.xml'))),'StaticText':Text,'_warderUiText':lambda s:s,'Writelog':lambda *_:None,'WarderProgramInfo':object()}
    code=compile(patch_nodes(),str(PLUGIN),'exec');exceptions=[]
    def trace(frame,event,arg):
        if event=='exception' and frame.f_code.co_filename==str(PLUGIN) and frame.f_code.co_name=='<module>':
            typ,error,_=arg;exceptions.append({'type':typ.__name__,'message':str(error),'line':frame.f_lineno})
        return trace
    old_trace=sys.gettrace()
    try:
        sys.settrace(trace);exec(code,env)
        # This runs upstream EPGSelection.__new__ in the modern case. Returning
        # a Grid object skips the compatibility class's patched __init__.
        obj=module.EPGSelection(None)
    finally:
        sys.settrace(old_trace)
        for name,previous in old_modules.items():
            if previous is None:sys.modules.pop(name,None)
            else:sys.modules[name]=previous
    present={key:obj[key].text for key in KEYS if key in obj}
    return {'api':'post-refactor' if modern else 'pre-refactor','created_class':type(obj).__name__,'visible_footer_sources':present,'source_count':len(present),'silently_suppressed_exceptions':exceptions}

def main():
    p=argparse.ArgumentParser();p.add_argument('--snapshots',type=Path,required=True);p.add_argument('--report',type=Path,required=True);args=p.parse_args()
    before=(args.snapshots/'EpgSelection-openatv-before.py').read_text();after=(args.snapshots/'EpgSelection-openatv-after.py').read_text()
    old=run_snapshot(before,after,False);new=run_snapshot(before,after,True)
    assert old['source_count']==4 and not old['silently_suppressed_exceptions']
    assert new['source_count']==0
    assert any(e['type']=='AttributeError' and 'RefreshColouredKeys' in e['message'] for e in new['silently_suppressed_exceptions'])
    screen=ET.fromstring(SKIN.read_text()).find("screen[@name='GraphicalEPGPIG']")
    h=int(screen.get('size').split(',')[1]);geometry=[]
    for key in KEYS:
        w=screen.find("widget[@source='%s']"%key);assert w is not None
        y=int(w.get('position').split(',')[1]);height=int(w.get('size').split(',')[1]);assert y+height<=h
        geometry.append({'source':key,'y':y,'height':height,'inside_screen':True})
    result={'status':'cause-reproduced','fullhdglass_version':'1.0.44','fullhdglass_source_commit':'29e0b99b8282670efd0ad5ce3fd3d7310a9f2e0a','unchanged_published_plugin_sha256':hashlib.sha256(PLUGIN.read_bytes()).hexdigest(),'upstream_refactor':{'commit':'ce3361e87258ca73f2743a088fe502e71fd3485a','date':'2026-10-24','title':'EPG: refactor screens, lists and configuration','url':'https://github.com/openatv/enigma2/commit/ce3361e87258ca73f2743a088fe502e71fd3485a'},'snapshot_revisions':{'before':'06de0c9cfe7c449f1327dfe7e3f6057448526945','after':'f3aa19683fbbe8350b8b6627a341e5581a42eb12'},'snapshot_sha256':{'before':hashlib.sha256(before.encode()).hexdigest(),'after':hashlib.sha256(after.encode()).hexdigest()},'legacy_result':old,'modern_result':new,'skin_footer_geometry':geometry,'cause':['Modern OpenATV constructs EPGSelectionGrid through EPGSelection.__new__. The patched legacy EPGSelection.__init__ therefore does not create warder_key_* sources.','RefreshColouredKeys was removed from the new API. The unguarded lookup raises AttributeError, swallowed by the outer except Exception: pass, and installation stops before the custom button handlers.','The XML still renders the four custom warder_key_* sources; without their creation, all four captions remain absent.'],'validation_scope':'Exact published patch; actual upstream modern metaclass/factory; minimal GUI/controller-interface stand-ins. No physical receiver access.','production_changed':False,'installed_receiver_build_identified':False}
    args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
