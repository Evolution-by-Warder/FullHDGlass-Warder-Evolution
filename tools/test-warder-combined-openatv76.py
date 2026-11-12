#!/usr/bin/env python3
"""OpenATV 7.6 Warder combined visual candidate -- no receiver claims."""
import xml.etree.ElementTree as ET
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
SK=ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml'
HD=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/hdg17Screens.xml'
P=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
root=ET.parse(SK).getroot()
for name in ('EPGvertical','EPGverticalPIG'):
    screens=root.findall("screen[@name='%s']"%name)
    assert len(screens)==1,(name,len(screens))
    screen=screens[0]
    assert screen.get('size')=='1920,1080'
    assert screen.get('position')=='0,0'
    assert screen.get('flags')=='wfNoBorder'
    assert screen.find("widget[@name='bouquetlist']") is not None
    assert screen.find("widget[@name='list']") is not None
    for i in range(1,6):
        l=screen.find("widget[@name='list%d']"%i)
        assert l is not None
        x,y=map(int,l.get('position').split(','))
        w,h=map(int,l.get('size').split(','))
        assert y==207 and h==610 and x>=45 and x+w<=1870
        assert screen.find("widget[@name='currCh%d']"%i) is not None
        assert screen.find("widget[@name='Active%d']"%i) is not None
    event=next(x for x in screen.findall('widget') if x.get('source')=='Event')
    y=int(event.get('position').split(',')[1])
    h=int(event.get('size').split(',')[1])
    assert y>=825 and h>=145 and y+h<=1000
    for color in ('red','green','yellow','blue'):
        assert screen.find("widget[@name='key_%s']"%color) is not None
    if name.endswith('PIG'):
        assert screen.find("widget[@render='Pig']") is not None
src=HD.read_text()
s=src.index('<screen name="ChannelSelection-12"')
part=src[s:src.index('</screen>',s)]
assert 'size="1920,1080"' in part
assert 'serviceNameFont="Prive4;28"' in part
assert 'serviceInfoFont="Prive4;25"' in part
for x in (60,520,980,1440):
    assert 'position="%d,110" size="420,90"'%(x+60) in part
    assert 'position="%d,108"'%x in part
assert 'source="selected_item" render="Label"' in (P/'plugin.py').read_text()
catalog=json.loads((P/'warder-spinners.json').read_text())
assert catalog['default']=='bakussa'
assert len(catalog['themes']['bakussa']['frames'])==20
print('PASS: fullscreen Vertical EPG + PiG, classic list, date preview and spinner')
