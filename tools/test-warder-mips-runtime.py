#!/usr/bin/env python3
"""Exercise actual MIPS renderer code with both Enigma timer APIs."""
import ast
import runpy
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

ROOT=Path(__file__).resolve().parents[1]/'source/package-root/usr/lib/enigma2/python'
P=runpy.run_path(str(ROOT/'Plugins/Extensions/setupGlass17/warderMipsRuntime.py'))

class Timer:
    def __init__(self, modern):
        self.active=False
        self.callbacks=[]
        self.callback=self.callbacks
        self.timeout=NS(connect=self.connect if modern else None,get=lambda:self.callbacks)
        if not modern:
            del self.timeout.connect
        self.starts=[]
    def connect(self,cb):
        self.callbacks.append(cb)
        return NS(disconnect=lambda:self.callbacks.remove(cb))
    def start(self,delay,*args):
        self.active=True
        self.starts.append(delay)
    def stop(self):
        self.active=False
    def isActive(self):
        return self.active

class Renderer:
    CHANGED_DEFAULT,CHANGED_CLEAR=0,2
    def __init__(self):self.instance=None;self.source=None
    def postWidgetCreate(self,instance):pass
    def preWidgetRemove(self,instance):pass
    def doSuspend(self,suspended):pass
    def destroy(self):self.__dict__.clear()

class VariableText:
    def __init__(self):self.text=''

def make(name,mips,modern):
    node=next(n for n in ast.parse((ROOT/'Components/Renderer'/(name+'.py')).read_text()).body if isinstance(n,ast.ClassDef))
    env=dict(Renderer=Renderer,VariableText=VariableText,eLabel=object,ePoint=lambda x,y:(x,y),
             eTimer=lambda:Timer(modern),HardwareInfo=lambda:NS(get_device_name=lambda:'test'),
             MIPS_RUNTIME=mips,RendererTimerGuard=P['RendererTimerGuard'])
    exec(compile(ast.Module(body=[node],type_ignores=[]),name,'exec'),env)
    obj=env[name]()
    obj.posX=obj.posY=10
    obj.source=NS(text='long programme name')
    timer=getattr(obj,'_g17RollName__moveLCD1Text' if name=='g17RollName' else 'rollTimerText')
    return obj,timer

def widget():
    return NS(calculateSize=lambda:NS(width=lambda:300),move=lambda point:None)

class Mips(unittest.TestCase):
    def test_architectures_and_budget(self):
        for m in ('mips','mipsel','MIPS64EL','mips32le'):
            self.assertTrue(P['is_mips'](m))
        for m in ('armv7l','arm','aarch64','x86_64','sh4','unknown','','not-mips'):
            self.assertFalse(P['is_mips'](m))
        for ram,n,delay in ((None,12,150),(128*1024,12,150),(256*1024,12,150),(512*1024,24,100)):
            frames=list(P['weather_frame_indices'](100,True,ram))
            self.assertEqual(len(frames),n)
            self.assertEqual((frames[0],frames[-1]),(0,99))
            self.assertEqual(frames,sorted(set(frames)))
            self.assertEqual(P['weather_delay'](50,True,ram),delay)
            self.assertEqual(list(P['weather_frame_indices'](100,False,ram)),list(range(100)))
            self.assertEqual(P['weather_delay'](50,False,ram),50)

    def test_mips_lifecycle(self):
        for name in ('g17RollName','g17RollerChar'):
            for modern in (True,False):
                obj,timer=make(name,True,modern)
                self.assertEqual(timer.callbacks,[])
                for _ in range(100):
                    obj.instance=widget()
                    obj.postWidgetCreate(obj.instance)
                    obj.postWidgetCreate(obj.instance)
                    self.assertEqual(len(timer.callbacks),1)
                    obj.doSuspend(False)
                    self.assertTrue(timer.active)
                    queued=timer.callbacks[0]
                    queued()
                    obj.doSuspend(True)
                    queued()
                    self.assertFalse(timer.active)
                    obj.changed((obj.CHANGED_DEFAULT,))
                    self.assertFalse(timer.active)
                    obj.doSuspend(False)
                    self.assertTrue(timer.active)
                    obj.changed((obj.CHANGED_CLEAR,))
                    self.assertFalse(timer.active)
                    obj.preWidgetRemove(obj.instance)
                    obj.instance=None
                    queued()
                    self.assertFalse(timer.active)
                    self.assertEqual(timer.callbacks,[])
                obj.destroy()
                queued()

    def test_non_mips_legacy_behaviour(self):
        for name,first,nxt in (('g17RollName',10000,90),('g17RollerChar',8500,250)):
            for modern in (True,False):
                obj,timer=make(name,False,modern)
                self.assertFalse(hasattr(obj,'_warder_timer_guard'))
                for method in ('postWidgetCreate','preWidgetRemove','doSuspend','destroy'):
                    self.assertIs(getattr(type(obj),method),getattr(Renderer,method))
                obj.instance=widget()
                obj.changed((obj.CHANGED_DEFAULT,))
                self.assertEqual(timer.starts[-1],first)
                timer.callbacks[0]()
                self.assertEqual(timer.starts[-1],nxt)

    def test_actual_infobar_animation_callbacks(self):
        tree=ast.parse((ROOT/'Plugins/Extensions/setupGlass17/plugin.py').read_text())
        cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ExtraInfo17')
        methods=[n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name in ('animTimerEvent','setOn','stopEcmCaidInfo')]
        self.assertEqual(len(methods),3)
        for mips in (True,False):
            scope=dict(MIPS_RUNTIME=mips,weather_delay=lambda delay:P['weather_delay'](delay,True,128*1024),
                       config=NS(plugins=NS(setupGlass17=NS(par170=NS(value=50),par57=NS(value='2')))))
            node=ast.ClassDef(name='ExtraInfo17',bases=[ast.Name(id='dict',ctx=ast.Load())],keywords=[],body=methods,decorator_list=[])
            exec(compile(ast.fix_missing_locations(ast.Module(body=[node],type_ignores=[])),'weather','exec'),scope)
            obj=scope['ExtraInfo17']()
            obj.timerpics=Timer(True)
            for name in ('iptvInfoRetryTimer','ecmCaidTimer','provRPMTimer','hddTimer'):
                setattr(obj,name,Timer(True))
            obj.chckWeaInafAnim=lambda:True
            obj._ExtraInfo17__warderScheduleIptvRetry=lambda:None
            obj.pics=['one','two']
            obj.slideXX=0
            frames=[]
            obj['picProvSat']=NS(instance=NS(setPixmap=frames.append))
            obj._ExtraInfo17__isOn=False
            obj.animTimerEvent()
            self.assertEqual(frames,[] if mips else ['one'])
            self.assertFalse(obj.timerpics.active)
            obj.setOn()
            self.assertEqual(obj.timerpics.starts[-1],150 if mips else 50)
            obj.animTimerEvent()
            self.assertEqual(obj.timerpics.starts[-1],150 if mips else 50)
            obj.stopEcmCaidInfo()
            self.assertEqual(obj.timerpics.active,not mips)
            if mips:
                obj['picProvSat'].instance=None
                obj.animTimerEvent()
                self.assertFalse(obj.timerpics.active)
                obj.pics=[]
                obj.setOn()
                self.assertFalse(obj.timerpics.active)


if __name__=='__main__':unittest.main()
