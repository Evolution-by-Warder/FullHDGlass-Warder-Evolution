#!/usr/bin/env python3
"""Replay native TimelineText layout and entries with a host list backend."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
from time import localtime, strftime
import unittest
import xml.etree.ElementTree as ET

spec=importlib.util.spec_from_file_location('row_fixture',Path(__file__).with_name('test-list-row-fit.py'))
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)


class Rect:
    def __init__(self,x,y,w,h):self.x,self.y,self.w,self.h=x,y,w,h
    def left(self):return self.x
    def width(self):return self.w


class Content:
    def __init__(self):self.row=25;self.fonts={};self.entries=[];self.widget=None
    def setSelectionClip(self,value):pass
    def setFont(self,index,value):self.fonts[index]=value
    def setItemHeight(self,value):
        self.row=value
        if self.widget is not None:self.widget.row=value
    def setList(self,entries):self.entries=entries


def create(height=45,width=1800,graphic=False,epg_type=5,active=True,hook=True):
    gui, menu, unused, parent=fixture.setup(active=active)
    if not hook:gui.applySkin=gui.applySkin.__wrapped__
    config=SimpleNamespace(epgselection=SimpleNamespace(**{
        name:SimpleNamespace(timelinefs=SimpleNamespace(value=0),timeline24h=SimpleNamespace(value=True))
        for name in ('grid','infobar')}))
    scope={'GUIComponent':gui,'eListbox':fixture.Listbox,'eListboxPythonMultiContent':Content,
           'eRect':Rect,'EPG_TYPE_GRAPH':5,'EPG_TYPE_INFOBARGRAPH':7,'getSkinFactor':lambda:1.5,
           'parseFont':lambda value,scale:SimpleNamespace(family=value.split(';')[0],pointSize=int(value.split(';')[1])),
           'parseColor':lambda value:SimpleNamespace(argb=lambda:0),
           'gFont':lambda family,size:SimpleNamespace(family=family,pointSize=size),
           'config':config,'loadPNG':lambda path:path,'resolveFilename':lambda scope,path:path,'SCOPE_GUISKIN':0,
           'time':lambda:1793558400,'localtime':localtime,'strftime':strftime,'_':lambda value:'Dnes' if value=='Today' else value,
           'RT_HALIGN_RIGHT':2,'RT_HALIGN_LEFT':1,'RT_VALIGN_CENTER':4,'MAX_TIMELINES':6,'BT_SCALE':1,
           'MultiContentEntryText':lambda **kwargs:dict(kind='text',**kwargs),
           'MultiContentEntryPixmapAlphaTest':lambda **kwargs:dict(kind='pixmap',**kwargs)}
    cls=fixture.native_class('Components/EpgList.py','TimelineText',scope)
    axis=cls(epgType=epg_type,graphic=graphic)
    axis.instance=fixture.Listbox(width,height,25)
    axis.l.widget=axis.instance
    axis.skinAttributes=[('size','%d,%d'%(width,height))]
    parent.clear();parent['timeline_text']=axis
    axis.applySkin(None,parent)
    for callback in parent.onLayoutFinish:callback()
    return axis,parent


class TimelineTests(unittest.TestCase):
    def test_original_axis_has_text_rect_taller_than_content_row(self):
        axis,parent=create(hook=False)
        self.assertEqual(axis.listHeight,45)
        self.assertEqual(axis.l.row,30)
        self.assertGreater(axis.listHeight,axis.l.row)

    def test_all_packaged_ruler_sizes_keep_full_allocated_height(self):
        tree=ET.parse(fixture.ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml')
        axes=[(screen.get('name'),widget) for screen in tree.findall('screen')
              for widget in screen.findall("widget[@name='timeline_text']")]
        self.assertGreaterEqual(len(axes),7)
        for name,widget in axes:
            width,height=map(int,widget.get('size').split(','))
            with self.subTest(screen=name):
                axis,parent=create(height,width)
                self.assertEqual(axis.instance.size().height(),height)
                self.assertEqual(axis.listHeight,height)
                self.assertEqual(axis.itemHeight,height)
                self.assertEqual(axis.l.row,height)

    def test_native_today_and_hour_entries_fit_same_single_row(self):
        for graphic in (False,True):
            for epg_type in (5,7):
                axis,parent=create(graphic=graphic,epg_type=epg_type)
                marker=lambda:SimpleNamespace(position=(0,0),setPosition=lambda x,y:None,
                    instance=SimpleNamespace(size=lambda:fixture.Size(28,100)),visible=False)
                grid=SimpleNamespace(getEventRect=lambda:Rect(200,0,1600,45),getTimeEpoch=lambda:240,
                    getTimeBase=lambda:1793558400,getServiceRect=lambda:Rect(0,0,200,45))
                axis.setEntries(grid,marker(),[marker() for unused in range(6)],True)
                labels=[entry for entry in axis.l.entries[0][1:] if entry['kind']=='text' and entry.get('text')]
                self.assertTrue(any(entry['text']=='Dnes' for entry in labels))
                self.assertTrue(any(':' in entry['text'] for entry in labels))
                self.assertTrue(all(entry['size'][1]==axis.l.row for entry in labels))

    def test_unrelated_skin_retains_native_axis_behavior(self):
        axis,parent=create(active=False)
        self.assertEqual(axis.l.row,30)
        self.assertEqual(axis.listHeight,45)

    def test_fullscreen_cool_guides_have_no_extra_window_frame(self):
        tree=ET.parse(fixture.ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml')
        for screen in tree.findall('screen'):
            if screen.get('name','').startswith('Cool') and screen.get('size')=='1920,1080':
                self.assertIn('wfNoBorder',screen.get('flags',''),screen.get('name'))


if __name__=='__main__':unittest.main(argv=[__file__]+fixture.rest)
