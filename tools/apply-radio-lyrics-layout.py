#!/usr/bin/env python3
"""Rebuild only the three owned radio screens; leave all TV XML byte-identical."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1]
SKIN=ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml'


def node(tag,**attrs):
    return '<'+tag+' '+ ' '.join(k+'="'+escape(str(v),{'"':'&quot;'})+'"' for k,v in attrs.items())+' />'


def panel(x,y,w,h,fill='#30102136'):
    out=[node('eLabel',position=f'{x},{y}',size=f'{w},{h}',backgroundColor=fill,zPosition=1)]
    for a,b,c,d in ((x,y,w,2),(x,y+h-2,w,2),(x,y,2,h),(x+w-2,y,2,h)):
        out.append(node('eLabel',position=f'{a},{b}',size=f'{c},{d}',backgroundColor='#003ccfff',zPosition=2))
    return out


def widget(source,render,x,y,w,h,font=None,convert=None,**kw):
    attrs=dict(source=source,render=render,position=f'{x},{y}',size=f'{w},{h}',transparent=1,zPosition=3)
    if font:attrs['font']='Regular;'+str(font)
    attrs.update(kw)
    plain=node('widget',**attrs)
    if convert:
        ctype,ctext=convert
        plain=plain[:-3]+'><convert type="'+ctype+'">'+escape(ctext)+'</convert></widget>'
    return plain


def footer(native=False,dy=0):
    out=panel(28,874-dy,1864,180,'#20102136')
    out += [node('eLabel',position=f'365,{894-dy}',size='1,138',backgroundColor='#0069cfe6',zPosition=2),
            node('eLabel',position=f'1420,{894-dy}',size='1,138',backgroundColor='#0069cfe6',zPosition=2)]
    out.append(widget('session.CurrentService','g17PicRef',88,904-dy,220,132,convert=('ServiceName','Reference'),alphatest='blend'))
    out.append(widget('session.CurrentService','Label',396,894-dy,980,47,38,('ServiceName','Name'),noWrap=1,foregroundColor='#00ffffff'))
    if native:
        out.append(widget('RdsDecoder','Label',396,950-dy,980,42,32,('RdsInfo','RadioText'),noWrap=1,foregroundColor='#00bce5ff'))
        out.append(widget('RdsDecoder','Label',396,1000-dy,980,36,27,('RdsInfo','RtpText'),noWrap=1,foregroundColor='#00d2d9e5'))
    else:
        out.append(node('widget',name='RadioText',position=f'396,{950-dy}',size='980,42',font='Regular;32',noWrap=1,foregroundColor='#00bce5ff',transparent=1,zPosition=3))
        out.append(node('widget',name='RtpText',position=f'396,{1000-dy}',size='980,36',font='Regular;27',noWrap=1,foregroundColor='#00d2d9e5',transparent=1,zPosition=3))
        # Keep the native-owned RASS widget contract without obstructing the picon.
        out.append(node('widget',name='RassLogo',pixmap='hd_glass17/icons/rass_logo.png',position=f'1370,{1005-dy}',size='32,16',alphatest='blend',zPosition=4))
    # Reuse the existing receiver-proven 350x126 animated spectrum unchanged.
    out.append(widget('session.CurrentService','WarderRadioSpectrum',1470,876-dy,350,126,alphatest='on'))
    out.append(widget('session.CurrentService','Label',1470,1009-dy,350,35,29,('WarderRadioServiceType','Type'),halign='center',noWrap=1,foregroundColor='#004feaff'))
    return out


def screen(name):
    if name == 'RadioInfoBar':
        return '<screen name="RadioInfoBar" position="0,874" size="1920,180" title="InfoBar" backgroundColor="transparent" flags="wfNoBorder">\n    '+'\n    '.join(footer(True,874))+'\n  </screen>'
    out=[node('ePixmap',pixmap='hd_glass17/warder-radio-background.jpg',position='0,0',size='1920,1080',zPosition=0,alphatest='off')]
    out+=panel(28,16,1864,86,'#20102136')
    out.append(node('eLabel',text='FullHDGlass by Warder',position='68,28',size='670,58',font='Regular;38',foregroundColor='#00ffffff',transparent=1,zPosition=3,valign='center'))
    out.append(widget('session.CurrentService','Label',850,28,250,58,40,('WarderRadioServiceType','Radio'),halign='center',valign='center',foregroundColor='#00ffffff'))
    for x,w,font,fmt in ((1310,280,32,'Format:%d. %m. %Y'),(1620,170,40,'Format:%H:%M'),(1790,78,29,'Format::%S')):
        out.append(widget('global.CurrentTime','Label',x,28,w,58,font,('ClockToText',fmt),halign='center',valign='center',noWrap=1,foregroundColor='#00ffffff'))
    out+=panel(306,136,440,720,'#90102136')
    out+=panel(766,136,860,720,'#18102136')
    out.append(widget('session.CurrentService','WarderRadioArtwork',316,146,420,700,alphatest='blend'))
    out.append(widget('session.CurrentService','Label',812,170,760,65,46,('WarderRadioServiceType','Lyrics'),foregroundColor='#00ffffff'))
    out.append(node('eLabel',position='812,250',size='760,2',backgroundColor='#004feaff',zPosition=3))
    out.append(widget('session.CurrentService','WarderRadioLyrics',812,285,760,530,34))
    out+=footer()
    return '<screen name="'+name+'" position="0,0" size="1920,1080" zPosition="-2" backgroundColor="transparent" flags="wfNoBorder">\n    '+'\n    '.join(out)+'\n  </screen>'


if __name__=='__main__':
    text=SKIN.read_text()
    for name in ('RdsInfoDisplay','RdsDisplay','RadioInfoBar'):
        pattern=r'<screen\b[^>]*name="'+name+r'"[^>]*>.*?</screen>'
        text,count=re.subn(pattern,lambda m:screen(name),text,flags=re.S)
        if count!=1:raise ValueError('Expected one '+name)
    SKIN.write_text(text)
