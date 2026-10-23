#!/usr/bin/env python3
"""Deterministic presentation-only upgrade of receiver settings screens."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/plugin.py'
FIXTURE=ROOT/'tools/fixtures/setup-ui-1.0.15.json'
SCREENS=('setupGlass17ScreenSetup','downloadMenu','satSelectorScr','warderPositionSelectorScr',
         'styleSelectorScr','selectScreenShowed','selectIconsDisplayed','historyScreen',
         'weatherCitySelector','cityFinder','dirBrowser')
BASE='#00071627';PANEL='#00102136';SELECT='#002a70ad';TEXT='#00ffffff';CYAN='#003ee8ff'
COLORS={'red':'#00ff526a','green':'#0039ff59','yellow':'#00f5d54e','blue':'#0045b9ff'}


def normalized(tree):
    tree=copy.deepcopy(tree)
    for cls in tree.body:
        if not isinstance(cls,ast.ClassDef) or cls.name not in SCREENS:continue
        for node in cls.body:
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='skin' for t in node.targets):
                node.value=ast.Constant('<presentation>')
        for node in ast.walk(cls):
            if isinstance(node,ast.keyword) and node.arg in ('color_sel','backcolor_sel'):
                node.value=ast.Constant('<selection-color>')
    def portable(value):
        if isinstance(value,ast.AST):
            # Python 3.12 adds type_params to definitions. Empty parameters
            # have no counterpart in the original Python 3.9 grammar.
            return [type(value).__name__,{field:portable(getattr(value,field,None))
                    for field in value._fields if field!='type_params' or getattr(value,field,None)}]
        if isinstance(value,list):return [portable(item) for item in value]
        if isinstance(value,bytes):return {'bytes_hex':value.hex()}
        return value
    serialized=json.dumps(portable(tree),sort_keys=True,separators=(',',':'),ensure_ascii=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


def widget_ids(root):
    return sorted((x.tag,x.get('name',''),x.get('source',''),x.get('render',''))
                  for x in root if x.tag=='widget')


def extract(text):
    result={}
    for cls in ast.parse(text).body:
        if not isinstance(cls,ast.ClassDef) or cls.name not in SCREENS:continue
        for node in cls.body:
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='skin' for t in node.targets):
                if isinstance(node.value,ast.Constant):result[cls.name]=(node,node.value.value)
    return result


def element(tag,x,y,w,h,**attributes):
    return ET.Element(tag,{'position':'%d,%d'%(x,y),'size':'%d,%d'%(w,h),**{k:str(v) for k,v in attributes.items()}})


def label(x,y,w,h,text='',size=28,color=TEXT,source=None,render='Label',**attributes):
    kw={'font':'Regular;%d'%size,'foregroundColor':color,'backgroundColor':PANEL,
        'transparent':'0','zPosition':'5','valign':'center','noWrap':'1',**attributes}
    if source:kw.update(source=source,render=render)
    else:kw['text']=text
    return element('widget' if source else 'eLabel',x,y,w,h,**kw)


def panel(root,x,y,w,h):
    root.insert(0,element('eLabel',x,y,w,h,backgroundColor=PANEL,zPosition='0'))
    for box in ((x,y,w,2),(x,y+h-2,w,2),(x,y,2,h),(x+w-2,y,2,h)):
        root.insert(1,element('eLabel',*box,backgroundColor=CYAN,zPosition='1'))


def header(root,download=False):
    root.append(label(60,25,900,65,'FullHDGlass',54,CYAN,backgroundColor=BASE))
    root.append(label(62,91,780,35,'Warder Evolution',29,TEXT,backgroundColor=BASE))
    root.append(label(1030,22,820,36,size=25,source='global.CurrentTime',render='g17dateFormat',
                             format='%A  %d. %B %Y',fTyp='4',halign='right',backgroundColor=BASE))
    clock=label(1500,63,240,65,size=52,source='global.CurrentTime',halign='right',backgroundColor=BASE)
    ET.SubElement(clock,'convert',{'type':'g17ClockToText'}).text='Default';root.append(clock)
    seconds=label(1745,82,105,42,size=34,source='global.CurrentTime',halign='right',backgroundColor=BASE)
    ET.SubElement(seconds,'convert',{'type':'g17ClockToText'}).text='Format::%S';root.append(seconds)
    root.append(element('eLabel',60,132,1800,2,backgroundColor=CYAN,zPosition='1'))


def themed(name,original):
    fragment=name=='selectIconsDisplayed'
    root=ET.fromstring(original+('</screen>' if fragment else ''))
    w,h=map(int,root.get('size').split(','));full=name in ('setupGlass17ScreenSetup','downloadMenu')
    stable_coordinates=name in ('historyScreen','selectIconsDisplayed')
    root.set('backgroundColor',BASE if full else PANEL);root.set('flags','wfNoBorder')
    if not full:root.set('position','center,center')
    # Preserve the dynamic footer moves in historyScreen and the icon widgets
    # appended by selectIconsDisplayed.__init__. Other popups gain a title band.
    shift=0 if full or stable_coordinates else 64
    if shift:root.set('size','%d,%d'%(w,h+88));h+=88
    for child in list(root):
        if child.tag=='eLabel':root.remove(child);continue
        if child.tag!='widget':continue
        if shift:
            x,y=map(int,child.get('position').split(','));child.set('position','%d,%d'%(x,y+shift))
        for key in ('shadowColor','shadowOffset','selectionPixmap'):
            child.attrib.pop(key,None)
        is_pixmap=(child.get('alphatest') is not None or child.get('render') in ('Pig','Canvas')
                   or child.get('name') in ('help_pict','helpPicon','helpPiconFrame','scr_preview'))
        if not is_pixmap:
            child.set('foregroundColor',TEXT);child.set('backgroundColor',PANEL);child.set('transparent','0')
        if child.get('scrollbarMode') is not None or child.get('name') in ('config','filelist'):
            child.set('scrollbarMode','showOnDemand')
            child.set('foregroundColorSelected',TEXT);child.set('backgroundColorSelected',SELECT)
    fields={x.get('name') or x.get('source'):x for x in root if x.tag=='widget'}
    keys=[x for x in root if (x.get('name') or x.get('source','')).startswith('key_')]
    keys.sort(key=lambda x:int(x.get('position').split(',')[0]))
    for index,key in enumerate(keys):
        color=(key.get('name') or key.get('source'))[4:]
        if color not in COLORS:continue
        # historyScreen moves the half-width red action when green is hidden.
        if name in ('historyScreen','setupGlass17ScreenSetup','selectIconsDisplayed'):
            x,y=map(int,key.get('position').split(','));wide=int(key.get('size').split(',')[0])
        else:
            gap=16;margin=20;wide=(w-2*margin-gap*(len(keys)-1))//len(keys)
            x=margin+index*(wide+gap);y=h-74
            key.set('position','%d,%d'%(x,y));key.set('size','%d,50'%wide)
        key.set('font','Regular;28');key.set('foregroundColor',COLORS[color]);key.set('backgroundColor',PANEL)
        key.set('halign','center');key.set('valign','center');key.set('noWrap','1');key.set('transparent','0')
        if 'line_'+color in fields:
            fields['line_'+color].set('backgroundColor',COLORS[color])
        else:root.append(element('eLabel',x,y-6,wide,2,backgroundColor=COLORS[color],zPosition='1'))
    if name=='setupGlass17ScreenSetup':
        fields['description'].set('position','60,142');fields['description'].set('size','1800,46')
        fields['description'].set('font','Regular;24');fields['description'].set('halign','left')
        fields['description'].set('foregroundColor','#00b5d4ec');fields['description'].set('backgroundColor',BASE)
        fields['session.VideoPicture'].set('position','60,210');fields['session.VideoPicture'].set('size','737,415')
        fields['list'].set('position','860,210');fields['list'].set('size','990,720')
        fields['config'].set('position','60,210');fields['config'].set('size','1800,440')
        fields['white'].set('backgroundColor',CYAN)
        for key in ('help_txt','helpTxtAnim'):
            fields[key].set('font','Regular;28');fields[key].set('foregroundColor','#00b5d4ec')
        fields['selected_item'].set('font','Regular;24')
        # Keep the existing Canvas/color and animated help previews visible.
        for key in ('selected_item','help_txt','helpTxtAnim'):
            fields[key].set('transparent','1')
        panel(root,50,200,760,760);panel(root,850,200,1010,760);header(root)
    elif name=='downloadMenu':
        fields['list'].set('position','50,175');fields['list'].set('size','1820,762')
        fields['dwn'].set('font','Regular;32');fields['dwn'].set('zPosition','20')
        panel(root,40,165,1840,810);header(root,True)
    else:
        if name=='historyScreen':
            fields['Changelog_info'].set('position','15,70');fields['Changelog_info'].set('size','1620,670')
        elif name=='selectIconsDisplayed':
            pass  # Appended preview/icon positions start at y=57.
        title_height=38 if fragment else 45
        root.append(label(20,5,w-40,title_height,size=27,color=CYAN,source='Title'))
        root.append(element('eLabel',20,48 if fragment else 57,w-40,2,backgroundColor=CYAN,zPosition='1'))
        for box in ((0,0,w,2),(0,h-2,w,2),(0,0,2,h),(w-2,0,2,h)):
            root.append(element('eLabel',*box,backgroundColor=CYAN,zPosition='5'))
    result='\n'.join(line.rstrip() for line in ET.tostring(root,encoding='unicode').splitlines())
    return result.removesuffix('</screen>') if fragment else result


def capture(text):
    skins=extract(text)
    return {'source_version':'1.0.15','source_commit':'5c09eb9688414971ddf9559e47938f8fccd32157',
            'logic_sha256':normalized(ast.parse(text)),
            'skins':{name:original for name,(node,original) in skins.items()}}


def apply():
    text=PLUGIN.read_text();snapshot=json.loads(FIXTURE.read_text())
    if normalized(ast.parse(text))!=snapshot['logic_sha256']:raise SystemExit('Unexpected settings logic; review baseline first')
    rows=text.splitlines(keepends=True);replacements=[]
    for name,(node,current) in extract(text).items():
        styled=themed(name,snapshot['skins'][name])
        replacements.append((node.lineno-1,node.end_lineno,'\tskin = """\n'+styled+'\n"""\n'))
    for start,end,value in sorted(replacements,reverse=True):rows[start:end]=[value]
    text=''.join(rows)
    # Selection colors in MultiContent rows are explicitly supplied by the
    # original controllers, so the shared XML colors alone cannot replace them.
    tree=ast.parse(text);lines=text.splitlines(keepends=True)
    for cls in tree.body:
        if isinstance(cls,ast.ClassDef) and cls.name in SCREENS:
            for i in range(cls.lineno-1,cls.end_lineno):
                lines[i]=lines[i].replace("color_sel=int('0xff9c00',16)","color_sel=int('0xffffff',16)")
                lines[i]=lines[i].replace('color_sel=int("0xff9c00",16)','color_sel=int("0xffffff",16)')
                lines[i]=lines[i].replace("color_sel=int('0xff3300', 16)","color_sel=int('0xffffff', 16)")
                lines[i]=lines[i].replace('backcolor_sel=0,','backcolor_sel=int(\'0x2a70ad\',16),')
    result=''.join(lines)
    if normalized(ast.parse(result))!=snapshot['logic_sha256']:raise SystemExit('Controller logic changed')
    PLUGIN.write_text(result)


if __name__=='__main__':apply()
