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
BASE='#00071627';PANEL='#00102136';GLASS='#1a102136';CLEAR='#ff000000';SELECT='#002a70ad';TEXT='#00ffffff';CYAN='#003ee8ff'
COLORS={'red':'#00ff526a','green':'#0039ff59','yellow':'#00f5d54e','blue':'#0045b9ff'}


# These are the only controller additions: registered panel widgets and a
# presentation-only switch. Normalize exact AST matches, never entire methods
# by name, so unexpected edits still fail the frozen business-logic guard.
PANEL_INIT = """for prefix, count in (("warder_menu_panel_", 10), ("warder_settings_panel_", 5)):
    for index in range(count):
        self[prefix + str(index)] = Label("")
        self[prefix + str(index)].hide()
"""
PANEL_MODE_OLD = 'def _warderSetPanelMode(self):\n    for prefix, count, visible in (("warder_menu_panel_", 10, self.isMainMenu), ("warder_settings_panel_", 5, not self.isMainMenu)):\n        for index in range(count):\n            panel = self[prefix + str(index)]\n            if visible:\n                panel.show()\n            else:\n                panel.hide()\n    if self.isMainMenu:\n        self["help_txt"].instance.resize(eSize(737, 248))\n    else:\n        self["help_txt"].instance.resize(eSize(780, 350))\n'
PANEL_MODE = 'def _warderSetPanelMode(self):\n    for prefix, count, visible in (("warder_menu_panel_", 10, self.isMainMenu), ("warder_settings_panel_", 5, not self.isMainMenu)):\n        for index in range(count):\n            panel = self[prefix + str(index)]\n            if visible:\n                panel.show()\n            else:\n                panel.hide()\n    if self.isMainMenu:\n        self["help_txt"].instance.resize(eSize(737, 248))\n    else:\n        self["help_txt"].instance.resize(eSize(780, 350))\n    for renderer in getattr(self, "renderer", ()):\n        if type(renderer).__name__ in ("Pig", "WarderSettingsPig") and renderer.instance is not None:\n            if self.isMainMenu:\n                renderer.onShow()\n                renderer.instance.show()\n            else:\n                renderer.onHide()\n                renderer.instance.hide()\n'
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
    old_method=portable(ast.parse(PANEL_MODE_OLD).body[0])
    expected_init=portable(ast.parse(PANEL_INIT).body[0])
    expected_call=portable(ast.parse(PANEL_CALL).body[0])
    expected_color=portable(ast.parse(COLOR_VISIBILITY).body[0])
    cls.body=[node for node in cls.body if portable(node) not in (expected_method,old_method)]
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



BANNER_GEOMETRY = (
    ('self["help_txt"].instance.move(ePoint(60,660))', 'self["help_txt"].instance.move(ePoint(60,692))'),

    ('self["key_red"].move(ePoint(412,775))', 'self["key_red"].move(ePoint(547,939))'),
    ('self["line_red"].move(ePoint(412,765))', 'self["line_red"].move(ePoint(547,929))'),
)
ICON_OLD = 'str(405+(x-off)*300)'
ICON_NEW = 'str(672+(x-off)*300)'
ICON_Y_OLD = 'str(57+y)'
ICON_Y_NEW = 'str(221+y)'
PREVIEW_OLD = 'position="481,96" size="768,432"'
PREVIEW_NEW = 'position="748,260" size="768,432"'


def strip_banner_geometry(tree):
    restores={json.dumps(portable(ast.parse(new).body[0]),sort_keys=True):ast.parse(old).body[0] for old,new in BANNER_GEOMETRY}
    icon_restores={json.dumps(portable(ast.parse(new,mode='eval').body),sort_keys=True):ast.parse(old,mode='eval').body for old,new in ((ICON_OLD,ICON_NEW),(ICON_Y_OLD,ICON_Y_NEW))}
    class Restore(ast.NodeTransformer):
        def visit_Expr(self,node):
            key=json.dumps(portable(node),sort_keys=True)
            if key in restores:return copy.deepcopy(restores[key])
            return self.generic_visit(node)
        def visit_Call(self,node):
            key=json.dumps(portable(node),sort_keys=True)
            if key in icon_restores:return copy.deepcopy(icon_restores[key])
            return self.generic_visit(node)
        def visit_Constant(self,node):
            if isinstance(node.value,str) and PREVIEW_NEW in node.value:
                node.value=node.value.replace(PREVIEW_NEW,PREVIEW_OLD)
            return node
    for cls in tree.body:
        if isinstance(cls,ast.ClassDef) and cls.name in ('setupGlass17ScreenSetup','historyScreen','selectIconsDisplayed'):
            for method in cls.body:
                if isinstance(method,ast.FunctionDef) and method.name in ('runSetup','readandshow','__init__'):Restore().visit(method)
    return tree


def strip_reviewed_batch(tree):
    # Exact reviewed AST replacements only. A changed save/action/installer node
    # no longer matches and therefore still trips the frozen 1.0.15 fingerprint.
    records=json.loads((ROOT/'design/settings-batch261-logic.json').read_text())
    mapping={(r['scope'],json.dumps(portable(ast.parse(r['after']).body[0]),sort_keys=True)):r['before'] for r in records}
    def restore(nodes, scope):
        result=[]
        for node in nodes:
            key=(scope,json.dumps(portable(node),sort_keys=True))
            if key in mapping:
                result.extend(ast.parse(mapping[key]).body)
            else:
                if isinstance(node,ast.ClassDef):node.body=restore(node.body,node.name)
                result.append(node)
        return result
    tree=copy.deepcopy(tree)
    tree.body=restore(tree.body,'module')
    return tree


def normalized(tree):
    tree=strip_reviewed_batch(tree)
    tree=strip_banner_geometry(tree)
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
    elif 'name' not in attributes:kw['text']=text
    return element('widget' if source or 'name' in attributes else 'eLabel',x,y,w,h,**kw)


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


BANNER_HEIGHT = 164
BANNER_IMAGE = '/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/images/warder-settings-background.png'


def header(root,download=False,context=False):
    # A static, native pixmap, decoded once when the screen opens. No work on
    # selection changes; panels above it retain their existing opaque fill.
    root.insert(0,element('ePixmap',0,0,1920,1080,pixmap=BANNER_IMAGE,scale='1',zPosition='0'))
    for x,y,w,h,font,fmt,align in ((1120,25,250,36,25,'Format:%A','right'),
                                   (1020,70,350,36,24,'Format:%d. %B %Y','right'),
                                   (1398,32,190,85,62,'Default','center'),
                                   (1590,58,66,54,38,'Format::%S','left')):
        text=label(x,y,w,h,size=font,source='global.CurrentTime',halign=align,transparent='1',
                   backgroundColor=BASE,shadowColor=BASE,shadowOffset='1,1')
        ET.SubElement(text,'convert',{'type':'g17ClockToText'}).text=fmt
        root.append(text)
    version=(PLUGIN.parent/'version').read_text().strip()
    root.append(label(1680,25,210,36,text='Version:',size=25,color=CYAN,halign='center',transparent='1',backgroundColor=BASE))
    root.append(label(1680,70,210,36,text=version,size=24,color=CYAN,halign='center',transparent='1',backgroundColor=BASE))
    for x in (1392,1664):root.append(element('eLabel',x,25,2,84,backgroundColor=CYAN,zPosition='5'))
    if context:
        root.append(label(850,120,700,38,size=25,color=CYAN,source='Title',halign='center',transparent='1',noWrap='1',backgroundColor=BASE,shadowColor=BASE,shadowOffset='1,1'))


def fullscreen_dialog(root,shift):
    """Keep the original control layout together below the common banner.

    Only the old popup decoration is replaced. A larger root makes the banner
    independent of popup size. Small menus retain their original control size.
    """
    w,h=map(int,root.get('size').split(','))
    old_body=h-(88 if shift else 0)
    dx=(1920-w)//2;dy=max(BANNER_HEIGHT,(1080-h)//2+shift)
    body=min(old_body,1080-dy)
    reduction=old_body-body
    for node in list(root):
        x,y=map(int,node.get('position').split(','));wide,high=map(int,node.get('size').split(','))
        key=node.get('name') or node.get('source','')
        if key=='Title':root.remove(node);continue
        if node.tag=='eLabel':
            # Keep only the existing coloured action underlines; the old
            # title divider and popup border are replaced by the body frame.
            if node.get('backgroundColor') not in COLORS.values():root.remove(node);continue
        y-=shift
        if key.startswith(('key_','line_')) or node.tag=='eLabel':y-=reduction
        if y+high>body:node.set('size','%d,%d'%(wide,max(1,body-y)))
        node.set('position','%d,%d'%(x+dx,y+dy))
        if node.tag=='widget':node.set('zPosition',str(max(4,int(node.get('zPosition','0')))))
    root.set('position','0,0');root.set('size','1920,1080');root.set('backgroundColor',BASE)
    panel(root,dx,dy,w,body)
    header(root,context=True)


def glass(root):
    """One translucent body layer; opaque menu panels keep LiveTV unchanged."""
    root.set('backgroundColor',CLEAR)
    for node in list(root):
        if node.tag=='ePixmap' and node.get('pixmap')==BANNER_IMAGE:
            root.remove(node)
    body=[]
    for node in root:
        key=node.get('name','');color=node.get('backgroundColor')
        x,y=map(int,node.get('position','0,0').split(','));w,h=map(int,node.get('size','0,0').split(','))
        if key.startswith('warder_menu_panel_'):continue
        if color==PANEL and w>=500 and h>=200 and (node.tag=='eLabel' or key=='warder_settings_panel_0'):
            if node.get('position')=='741,244' and node.get('size')=='960,540':continue
            node.set('backgroundColor',GLASS);node.set('zPosition','-1');body.append((x,y,w,h));continue
        if key.startswith('key_') and y>=980:
            node.set('backgroundColor',BASE);node.set('transparent','0');continue
        if color==PANEL and node.tag in ('widget','eLabel') and node.get('render') not in ('Canvas','WarderSettingsCanvas') and not node.get('alphatest'):
            node.set('backgroundColor',CLEAR);node.set('transparent','1')
        if node.get('scrollbarMode'):
            node.set('scrollbarBackgroundColor',PANEL);node.set('scrollbarForegroundColor',CYAN)
    root.insert(0,element('widget',0,0,1920,BANNER_HEIGHT,source='global.CurrentTime',render='WarderSettingsHeader',zPosition='-3'))
    if body:
        x,y,w,h=max(body,key=lambda box:box[2]*box[3])
        for bounds in ((0,BANNER_HEIGHT,1920,max(0,y-BANNER_HEIGHT)),(0,y,x,h),(x+w,y,1920-x-w,h),(0,y+h,1920,1080-y-h)):
            if bounds[2]>0 and bounds[3]>0:root.append(element('eLabel',*bounds,backgroundColor=BASE,zPosition='-2'))
    return root


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
        fields['description'].set('position','60,174');fields['description'].set('size','1800,46')
        fields['description'].set('font','Regular;24');fields['description'].set('halign','left')
        fields['description'].set('foregroundColor','#00b5d4ec');fields['description'].set('backgroundColor',BASE)
        fields['session.VideoPicture'].set('render','WarderSettingsPig')
        fields['session.VideoPicture'].set('position','60,242');fields['session.VideoPicture'].set('size','737,415')
        fields['list'].set('position','860,238');fields['list'].set('size','990,720')
        fields['config'].set('position','60,242');fields['config'].set('size','1790,320')
        fields['white'].set('backgroundColor',CYAN)
        fields['white'].set('size','1790,2');fields['white'].set('position','60,574')
        # Keep the 882:300 artwork ratio with padding on all four sides.
        fields['help_pict'].set('alphatest','blend');fields['help_pict'].set('position','445,592');fields['help_pict'].set('size','1029,350')
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
        switchable_panel(root,'warder_menu_panel_',50,232,760,728,0)
        # Continue numbering the right-hand panel in the same visibility group.
        switchable_panel(root,'warder_menu_right_',850,232,1010,728,0)
        for node in root:
            key=node.get('name','')
            if key.startswith('warder_menu_right_'):
                node.set('name','warder_menu_panel_'+str(5+int(key.rsplit('_',1)[1])))
        switchable_panel(root,'warder_settings_panel_',50,232,1810,728,2)
        # All config/help content must be above the settings panel and border.
        for key in ('config','help_pict','help_txt','helpTxtAnim','white'):
            fields[key].set('zPosition','4')
        header(root)
    elif name=='downloadMenu':
        fields['list'].set('position','50,207');fields['list'].set('size','1820,730')
        fields['list'].set('zPosition','2')
        fields['dwn'].set('position','50,166');fields['dwn'].set('size','1820,30')
        fields['dwn'].set('font','Regular;25');fields['dwn'].set('zPosition','20')
        panel(root,40,197,1840,778);header(root,True)
    else:
        if name=='historyScreen':
            fields['Changelog_info'].set('position','15,70');fields['Changelog_info'].set('size','1620,670')
        elif name=='selectIconsDisplayed':
            # After the 164 px body offset, both list and preview center at y=476.
            fields['list'].set('position','45,127');fields['list'].set('size','315,370')
        title_height=38 if fragment else 45
        root.append(label(20,5,w-40,title_height,size=27,color=CYAN,source='Title'))
        root.append(element('eLabel',20,48 if fragment else 57,w-40,2,backgroundColor=CYAN,zPosition='1'))
        for box in ((0,0,w,2),(0,h-2,w,2),(0,0,2,h),(w-2,0,2,h)):
            root.append(element('eLabel',*box,backgroundColor=CYAN,zPosition='5'))
    if not full:fullscreen_dialog(root,shift)
    if name=='historyScreen':
        # Content ends at 960; all actions are below the cyan frame.
        for node in root:
            key=node.get('name','')
            if key in ('key_red','key_green'):
                x=int(node.get('position').split(',')[0]);node.set('position','%d,1006'%x)
                node.set('backgroundColor',BASE)
            elif key in ('line_red','line_green'):
                x=int(node.get('position').split(',')[0]);node.set('position','%d,996'%x)
            elif node.tag=='eLabel' and node.get('size')=='1650,825':node.set('size','1650,796')
            elif node.tag=='eLabel' and node.get('size')=='2,825':node.set('size','2,796')
            elif node.tag=='eLabel' and node.get('position')=='135,987':node.set('position','135,958')
        fields['Changelog_info'].set('position','150,194');fields['Changelog_info'].set('size','1620,740')
    if name=='selectScreenShowed':
        fields['list'].set('size','495,585')
        preview=fields['scr_preview'];preview.set('backgroundColor',PANEL);preview.set('alphatest','off')
        # Opaque backing prevents transparent screenshots exposing arbitrary TV.
        root.insert(1,element('eLabel',741,244,960,540,backgroundColor=PANEL,zPosition='3'))
    glass(root)
    result='\n'.join(line.rstrip() for line in ET.tostring(root,encoding='unicode').splitlines())
    return result.removesuffix('</screen>') if fragment else result


def dialog_skin(kind):
    root=ET.Element('screen',name='WarderSettings'+kind,position='0,0',size='1920,1080',flags='wfNoBorder',backgroundColor=BASE)
    panel(root,135,184,1650,776)
    header(root,context=True)
    if kind=='Message':
        root.append(element('widget',170,220,70,70,name='icon',pixmaps=','.join('icons/input_'+x+'.png' for x in ('question','info','warning','error','message')),scale='1',alphatest='blend',conditional='icon',zPosition='4'))
        root.append(label(260,220,1480,520,size=30,name='text',noWrap='0'))
        root.append(element('widget',260,770,1480,160,name='list',font='Regular;30',itemHeight='50',scrollbarMode='showOnDemand',backgroundColor=PANEL,foregroundColor=TEXT,foregroundColorSelected=TEXT,backgroundColorSelected=SELECT,transparent='0',zPosition='4',conditional='list'))
    elif kind=='Choice':
        root.append(element('widget',165,214,1590,650,name='list',font='Regular;32',itemHeight='58',scrollbarMode='showOnDemand',backgroundColor=PANEL,foregroundColor=TEXT,foregroundColorSelected=TEXT,backgroundColorSelected=SELECT,transparent='0',zPosition='4'))
        root.append(label(165,885,1590,45,name='hint',size=26,halign='center'))
    else:
        root.append(label(180,270,1560,120,name='text',size=32,noWrap='0'))
        root.append(element('widget',180,430,1560,70,name='input',font='Regular;34',backgroundColor=BASE,foregroundColor=TEXT,zPosition='4'))
    for key,x in (('red',135),('green',968)):
        root.append(element('widget',x+308,996,200,2,name='line_'+key,backgroundColor=COLORS[key],zPosition='5'))
        root.append(label(x,1006,817,50,name='key_'+key,color=COLORS[key],halign='center',backgroundColor=BASE))
    return ET.tostring(glass(root),encoding='unicode')


def write_dialog_skins():
    data='# Generated by tools/style-setup-screens.py; do not edit.\n'
    for constant,kind in (('MESSAGE_SKIN','Message'),('CHOICE_SKIN','Choice'),('INPUT_SKIN','Input')):
        data+=constant+' = '+repr(dialog_skin(kind))+'\n'
    (PLUGIN.parent/'warderDialogSkins.py').write_text(data)


def capture(text):
    skins=extract(text)
    return {'source_version':'1.0.15','source_commit':'5c09eb9688414971ddf9559e47938f8fccd32157',
            'logic_sha256':normalized(ast.parse(text)),
            'skins':{name:original for name,(node,original) in skins.items()}}


def apply():
    text=PLUGIN.read_text();snapshot=json.loads(FIXTURE.read_text())
    old_block=''.join('\t'+line+'\n' for line in PANEL_MODE_OLD.splitlines())
    new_block=''.join('\t'+line+'\n' for line in PANEL_MODE.splitlines())
    if new_block not in text:text=text.replace(old_block,new_block)
    text=text.replace('eSize(737, 280)','eSize(737, 248)')
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
    for old,new in BANNER_GEOMETRY:
        # Original methods use both single and double quotes.
        result=result.replace(old,new).replace(old.replace('"',"'"),new).replace(old.replace(',',', '),new)
    result=result.replace(ICON_OLD,ICON_NEW).replace(ICON_Y_OLD,ICON_Y_NEW).replace(PREVIEW_OLD,PREVIEW_NEW)
    if normalized(ast.parse(result))!=snapshot['logic_sha256']:raise SystemExit('Unexpected banner geometry/controller change')
    PLUGIN.write_text(result)
    write_dialog_skins()


if __name__=='__main__':apply()
