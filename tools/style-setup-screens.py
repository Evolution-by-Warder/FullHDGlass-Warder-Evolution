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


# These are the only controller additions: registered panel widgets and a
# presentation-only switch. Normalize exact AST matches, never entire methods
# by name, so unexpected edits still fail the frozen business-logic guard.
PANEL_INIT = """for prefix, count in (("warder_menu_panel_", 10), ("warder_settings_panel_", 5)):
    for index in range(count):
        self[prefix + str(index)] = Label("")
        self[prefix + str(index)].hide()
"""
PANEL_MODE = """def _warderSetPanelMode(self):
    for prefix, count, visible in (("warder_menu_panel_", 10, self.isMainMenu), ("warder_settings_panel_", 5, not self.isMainMenu)):
        for index in range(count):
            panel = self[prefix + str(index)]
            if visible:
                panel.show()
            else:
                panel.hide()
    if self.isMainMenu:
        self["help_txt"].instance.resize(eSize(737, 280))
    else:
        self["help_txt"].instance.resize(eSize(780, 350))
"""
COLOR_VISIBILITY = 'self.canvas.warder_sample_visible = c is not None and not self.isMainMenu'
PANEL_CALL = 'self._warderSetPanelMode()'


def portable(value):
    if isinstance(value,ast.AST):
        # Python 3.12 adds type_params to definitions. Empty parameters
        # have no counterpart in the original Python 3.9 grammar.
        return [type(value).__name__,{field:portable(getattr(value,field,None))
                for field in value._fields if field!='type_params' or getattr(value,field,None)}]
    if isinstance(value,list):return [portable(item) for item in value]
    if isinstance(value,bytes):return {'bytes_hex':value.hex()}
    return value


def strip_panel_presentation(cls):
    expected_method=portable(ast.parse(PANEL_MODE).body[0])
    expected_init=portable(ast.parse(PANEL_INIT).body[0])
    expected_call=portable(ast.parse(PANEL_CALL).body[0])
    expected_color=portable(ast.parse(COLOR_VISIBILITY).body[0])
    cls.body=[node for node in cls.body if portable(node)!=expected_method]
    for node in cls.body:
        if isinstance(node,ast.FunctionDef) and node.name in ('__init__','runSetup','sampleColor'):
            exact={'__init__':expected_init,'runSetup':expected_call,'sampleColor':expected_color}[node.name]
            node.body=[child for child in node.body if portable(child)!=exact]


RESET_OLD = '_("Reset all settings of FHDG 17")'
RESET_NEW = RESET_OLD + '.replace("FHDG 17", "FullHDGlass")'


def strip_branding_presentation(tree):
    class ResetLabel(ast.NodeTransformer):
        def visit_Call(self,node):
            if portable(node)==portable(ast.parse(RESET_NEW,mode='eval').body):
                return ast.parse(RESET_OLD,mode='eval').body
            return self.generic_visit(node)
    tree=ResetLabel().visit(tree)
    for node in tree.body:
        if isinstance(node,ast.FunctionDef) and node.name in ('startSetup17','Plugins'):
            for child in ast.walk(node):
                if isinstance(child,ast.Constant) and child.value==' (FullHDGlass)':child.value=' (FHDG 17)'
                if node.name=='Plugins' and isinstance(child,ast.Call) and isinstance(child.func,ast.Name) and child.func.id=='PluginDescriptor':
                    for key in child.keywords:
                        if key.arg=='name' and isinstance(key.value,ast.Constant) and key.value.value=='FullHDGlass - Warder Evolution':
                            key.value.value='setupGlass17'
        if isinstance(node,ast.ClassDef) and node.name=='setupGlass17ScreenSetup':
            for method in node.body:
                if isinstance(method,ast.FunctionDef) and method.name=='getCurrentEntry':
                    for child in ast.walk(method):
                        if isinstance(child,ast.Constant) and child.value=='FullHDGlass':child.value='Full HD Glass17'
    return tree


VALUE_OLD = 'if ed:\n    self["selected_item"].setText("")\nelse:\n    self["selected_item"].setText(self.getCurrentValue())'
VALUE_NEW = 'if ed:\n    self["selected_item"].setText("")\nelse:\n    self["selected_item"].setText("")'


def strip_duplicate_value_presentation(tree):
    expected=portable(ast.parse(VALUE_NEW).body[0])
    class RestoreValue(ast.NodeTransformer):
        def visit_If(self,node):
            if portable(node)==expected:return ast.parse(VALUE_OLD).body[0]
            return self.generic_visit(node)
    for cls in tree.body:
        if isinstance(cls,ast.ClassDef) and cls.name=='setupGlass17ScreenSetup':
            for method in cls.body:
                if isinstance(method,ast.FunctionDef) and method.name=='doMyHelpWindow':RestoreValue().visit(method)
    return tree


HELP_NATIVE = 'self["help_pict"].instance.setPixmapFromFile(filename)'
HELP_CALL = 'self._warderLoadHelpPicture(filename)'
HELP_METHOD = """def _warderLoadHelpPicture(self, filename):
    from .warderHelpPreview import PreviewLoader
    if not hasattr(self, "_warderHelpLoader"):
        self._warderHelpLoader = PreviewLoader(self["help_pict"].instance.setPixmapFromFile)
        self.onClose.append(self._warderHelpLoader.close)
    self._warderHelpLoader.request(filename)
"""


def strip_help_background_presentation(tree):
    expected_method=portable(ast.parse(HELP_METHOD).body[0])
    expected_call=portable(ast.parse(HELP_CALL).body[0])
    class RestoreLoader(ast.NodeTransformer):
        def visit_Expr(self,node):
            if portable(node)==expected_call:return ast.parse(HELP_NATIVE).body[0]
            return self.generic_visit(node)
    for cls in tree.body:
        if isinstance(cls,ast.ClassDef) and cls.name=='setupGlass17ScreenSetup':
            cls.body=[node for node in cls.body if portable(node)!=expected_method]
            for node in cls.body:
                if isinstance(node,ast.FunctionDef) and node.name=='doMyHelpWindow':RestoreLoader().visit(node)
    return tree


GEOMETRY_OLD = 'self["help_txt"].instance.move(ePoint(579,660))'
GEOMETRY_NEW = 'self["help_txt"].instance.move(ePoint(579,592))'
VALUE_LABEL = 'self["selected_item"] = Label("")'
VALUE_SOURCE = 'self["selected_item"] = StaticText("")'


def strip_help_geometry_presentation(tree):
    expected_move=portable(ast.parse(GEOMETRY_NEW).body[0])
    expected_source=portable(ast.parse(VALUE_SOURCE).body[0])
    class RestoreGeometry(ast.NodeTransformer):
        def visit_Expr(self,node):
            if portable(node)==expected_move:return ast.parse(GEOMETRY_OLD).body[0]
            return self.generic_visit(node)
        def visit_Assign(self,node):
            if portable(node)==expected_source:return ast.parse(VALUE_LABEL).body[0]
            return self.generic_visit(node)
    for cls in tree.body:
        if isinstance(cls,ast.ClassDef) and cls.name=='setupGlass17ScreenSetup':
            for method in cls.body:
                if isinstance(method,ast.FunctionDef) and method.name in ('runSetup','__init__'):RestoreGeometry().visit(method)
    return tree


def normalized(tree):
    tree=strip_help_geometry_presentation(strip_help_background_presentation(strip_duplicate_value_presentation(strip_branding_presentation(copy.deepcopy(tree)))))
    for cls in tree.body:
        if not isinstance(cls,ast.ClassDef) or cls.name not in SCREENS:continue
        if cls.name=='setupGlass17ScreenSetup':strip_panel_presentation(cls)
        for node in cls.body:
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='skin' for t in node.targets):
                node.value=ast.Constant('<presentation>')
        for node in ast.walk(cls):
            if isinstance(node,ast.keyword) and node.arg in ('color_sel','backcolor_sel'):
                node.value=ast.Constant('<selection-color>')
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


def switchable_panel(root,prefix,x,y,w,h,z):
    boxes=((x,y,w,h),(x,y,w,2),(x,y+h-2,w,2),(x,y,2,h),(x+w-2,y,2,h))
    for index,box in enumerate(boxes):
        root.append(element('widget',*box,name=prefix+str(index),
                            backgroundColor=PANEL if index==0 else CYAN,
                            transparent='0',zPosition=str(z if index==0 else z+1)))


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
        root.set('title','FullHDGlass')
        for key in ('key_red','key_green'):
            fields[key].set('backgroundColor',BASE)
        fields['description'].set('position','60,142');fields['description'].set('size','1800,46')
        fields['description'].set('font','Regular;24');fields['description'].set('halign','left')
        fields['description'].set('foregroundColor','#00b5d4ec');fields['description'].set('backgroundColor',BASE)
        fields['session.VideoPicture'].set('position','60,210');fields['session.VideoPicture'].set('size','737,415')
        fields['list'].set('position','860,210');fields['list'].set('size','990,720')
        fields['config'].set('position','60,210');fields['config'].set('size','1790,360')
        fields['white'].set('backgroundColor',CYAN)
        fields['white'].set('size','1790,2');fields['white'].set('position','60,574')
        # Keep the 882:300 artwork ratio with padding on all four sides.
        fields['help_pict'].set('position','445,592');fields['help_pict'].set('size','1029,350')
        for key in ('help_txt','helpTxtAnim'):
            fields[key].set('position','579,592');fields[key].set('size','780,350')
        for key in ('help_txt','helpTxtAnim'):
            fields[key].set('font','Regular;28');fields[key].set('foregroundColor','#00b5d4ec')
        root.remove(fields['selected_item'])  # Removed from every setup group, not hidden beneath another widget.
        fields['helpPiconFrame'].set('position','865,705')
        fields['helpPicon'].set('position','885,721')
        canvas=fields['Canvas']
        canvas.set('render','WarderSettingsCanvas');canvas.set('backgroundColor',PANEL)
        canvas.set('position','735,890');canvas.set('zPosition','6')
        # Keep the existing Canvas/color and animated help previews visible.
        for key in ('help_txt','helpTxtAnim'):
            fields[key].set('transparent','1')
        switchable_panel(root,'warder_menu_panel_',50,200,760,760,0)
        # Continue numbering the right-hand panel in the same visibility group.
        switchable_panel(root,'warder_menu_right_',850,200,1010,760,0)
        for node in root:
            key=node.get('name','')
            if key.startswith('warder_menu_right_'):
                node.set('name','warder_menu_panel_'+str(5+int(key.rsplit('_',1)[1])))
        switchable_panel(root,'warder_settings_panel_',50,200,1810,760,2)
        # All config/help content must be above the settings panel and border.
        for key in ('config','help_pict','help_txt','helpTxtAnim','white'):
            fields[key].set('zPosition','4')
        header(root)
    elif name=='downloadMenu':
        fields['list'].set('position','50,175');fields['list'].set('size','1820,762')
        fields['list'].set('zPosition','2')
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
    if 'def _warderSetPanelMode(self):' not in text:
        init=''.join('\t\t'+line+'\n' for line in PANEL_INIT.splitlines())
        method=''.join('\t'+line+'\n' for line in PANEL_MODE.splitlines())
        start=text.index('class setupGlass17ScreenSetup(')
        before,owned=text[:start],text[start:]
        owned=owned.replace('\t\tself.list = [ ]',init+'\t\tself.list = [ ]',1)
        owned=owned.replace('\tdef runSetup(self):',method+'\n\tdef runSetup(self):\n\t\t'+PANEL_CALL,1)
        text=before+owned
    if COLOR_VISIBILITY not in text:
        text=text.replace('\tdef sampleColor(self, c):','\tdef sampleColor(self, c):\n\t\t'+COLOR_VISIBILITY,1)
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
    if RESET_NEW not in result:result=result.replace(RESET_OLD,RESET_NEW)
    result=result.replace('" (FHDG 17)"','" (FullHDGlass)"')
    result=result.replace('PluginDescriptor(name="setupGlass17"','PluginDescriptor(name="FullHDGlass - Warder Evolution"')
    result=result.replace('tmp = "Full HD Glass17"','tmp = "FullHDGlass"')
    if normalized(ast.parse(result))!=snapshot['logic_sha256']:raise SystemExit('Branding changed controller logic')
    result=result.replace('self["selected_item"].setText(self.getCurrentValue())','self["selected_item"].setText("")')
    if normalized(ast.parse(result))!=snapshot['logic_sha256']:raise SystemExit('Unexpected help controller change')
    if 'def _warderLoadHelpPicture(self, filename):' not in result:
        result=result.replace(HELP_NATIVE,HELP_CALL,1)
        method=''.join('\t'+line+'\n' for line in HELP_METHOD.splitlines())
        result=result.replace('\tdef readVersion(self):',method+'\n\tdef readVersion(self):',1)
    if normalized(ast.parse(result))!=snapshot['logic_sha256']:raise SystemExit('Unexpected background controller change')
    result=result.replace(GEOMETRY_OLD,GEOMETRY_NEW).replace("self['help_txt'].instance.move(ePoint(579,660))",GEOMETRY_NEW).replace(VALUE_LABEL,VALUE_SOURCE)
    if normalized(ast.parse(result))!=snapshot['logic_sha256']:raise SystemExit('Unexpected footer/geometry logic change')
    PLUGIN.write_text(result)


if __name__=='__main__':apply()

