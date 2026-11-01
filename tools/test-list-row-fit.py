#!/usr/bin/env python3
"""Check native GUI/MenuList integration and every packaged static list geometry."""
import argparse
import ast
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--upstream', required=True, type=Path)
args, rest = parser.parse_known_args()
PLUGIN = ROOT / 'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
spec = importlib.util.spec_from_file_location('row_fit', PLUGIN / 'warderListRows.py')
fit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fit)


class Size:
    def __init__(self, width, height): self.w, self.h = width, height
    def width(self): return self.w
    def height(self): return self.h


class Listbox:
    orVertical, orHorizontal, orGrid = 1, 2, 3
    def __init__(self, width=1560, height=615, row=45):
        self.dimensions = Size(width, height)
        self.row = row
        self.orientation = self.orVertical
        self.resize_calls = []
        self.index = self.top = 0
        self.items = list(range(80))
        self.font = 'Prive3;34'
    def size(self): return self.dimensions
    def getItemHeight(self): return self.row
    def getOrientation(self): return self.orientation
    def resize(self, size):
        self.dimensions = size
        self.resize_calls.append((size.width(), size.height()))
    def hide(self): pass
    def getCurrentIndex(self): return self.index
    def moveSelectionTo(self, index):
        self.index = max(0, min(index, len(self.items)-1))
        page = self.size().height() // self.row
        self.top = self.index // page * page
    def goPageDown(self): self.moveSelectionTo(self.index + self.size().height() // self.row)
    def goLineDown(self): self.moveSelectionTo(self.index+1)
    def goLineUp(self): self.moveSelectionTo(self.index-1)
    def partial_rows(self):
        return [(index, min(self.row, self.size().height() - (index-self.top)*self.row))
                for index in range(self.top, len(self.items))
                if 0 < self.size().height() - (index-self.top)*self.row < self.row]


class Label:
    def __init__(self, height=45, font=33):
        self.dimensions = Size(1220, height)
        self.font = SimpleNamespace(pointSize=font)
        self.nowrap = 0
        self.text = 'TV - Skylink CZ/SK > Kontextové menu pre zoznam kanálov > TV - Skylink CZ/SK'
    def size(self): return self.dimensions
    def getFont(self): return self.font
    def setNoWrap(self, value): self.nowrap = value
    def hide(self): pass


def native_class(path, name, scope):
    node = next(n for n in ast.parse((args.upstream/path).read_text()).body
                if isinstance(n, ast.ClassDef) and n.name == name)
    env = dict(scope)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(args.upstream/path), 'exec'), env)
    return env[name]


def apply_attributes(instance, desktop, attributes, scale):
    for name, value in attributes:
        if name == 'size':
            w, h = map(int, value.split(','))
            instance.resize(Size(w*scale[0][0]//scale[0][1], h*scale[1][0]//scale[1][1]))
        elif name == 'itemHeight': instance.row = int(value)*scale[1][0]//scale[1][1]
        elif name == 'listOrientation': instance.orientation = {'vertical':1,'horizontal':2,'grid':3}[value]


class Parent(dict):
    def __init__(self):
        super().__init__()
        self.onLayoutFinish, self.onShow, self.renderer = [], [], []
        self.scale = ((1,1),(1,1))
    def close(self): pass


def setup(active=True):
    gui = native_class('Components/GUIComponent.py', 'GUIComponent', {
        'eSize':Size, 'ePoint':Size, 'applyAllAttributes':apply_attributes})
    menu = native_class('Components/MenuList.py', 'MenuList', {
        'GUIComponent':gui, 'eListbox':Listbox,
        'eListboxPythonStringContent':lambda:SimpleNamespace(setList=lambda values:None)})
    fit.install(gui, lambda:active, Listbox, Size, Label)
    component = menu(list(range(80)))
    component.instance = Listbox()
    component.skinAttributes = [('size','1560,615'),('itemHeight','45')]
    parent = Parent(); parent['config'] = component
    return gui, menu, component, parent


def static_lists():
    payload = ROOT / 'source/package-root'
    for path in payload.rglob('*'):
        if path.suffix == '.xml':
            try: roots = [ET.parse(path).getroot()]
            except ET.ParseError: continue
        elif path.suffix == '.py':
            try: tree = ast.parse(path.read_text())
            except (SyntaxError, UnicodeError): continue
            roots = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value,str) and '<screen' in node.value:
                    try: roots.append(ET.fromstring(node.value.strip()))
                    except ET.ParseError: pass  # Dynamically assembled XML is checked at runtime.
        else: continue
        for root in roots:
            screens = [root] if root.tag == 'screen' else root.iter('screen')
            for screen in screens:
                for widget in screen.iter('widget'):
                    if widget.get('itemHeight','').isdigit():
                        try: width, height = map(int, widget.get('size','').split(','))
                        except ValueError: continue
                        if widget.get('listOrientation','vertical') != 'vertical': continue
                        if widget.get('itemSpacing','0,0').strip('0, '): continue
                        yield path.relative_to(payload).as_posix(), screen.get('name'), widget, width, height, int(widget.get('itemHeight'))


class ListFitTests(unittest.TestCase):
    def native_screen_layout(self, gui, parent):
        # Keep the exact method body, without parsing unrelated native match/case
        # methods on the Python 3.9 packaging worker.
        lines=(args.upstream/'Screens/Screen.py').read_text().splitlines(keepends=True)
        start=next(i for i,line in enumerate(lines) if line.startswith('\tdef createGUIScreen('))
        end=next((i for i in range(start+1,len(lines)) if lines[i].startswith('\tdef ')),len(lines))
        source=ast.parse(dedent(''.join(lines[start:end])))
        method=source.body[0]
        scope={'GUIComponent':gui,'applyAllAttributes':apply_attributes}
        exec(compile(ast.Module(body=[method],type_ignores=[]),'native-Screen-createGUIScreen','exec'),scope)
        parent.stacks=[];parent.additionalWidgets=[];parent.screenImage=None;parent.ignoreWidgets=[]
        scope['createGUIScreen'](parent,None,None,updateonly=True)

    def test_original_plain_callback_reproduces_exact_startup_crash(self):
        gui, menu, component, parent=setup()
        parent.onLayoutFinish.append(lambda: None)
        with self.assertRaisesRegex(TypeError,'exec\\(\\) arg 1 must be a string, bytes or code object'):
            self.native_screen_layout(gui,parent)

    def test_native_startup_layout_accepts_bound_callback_and_can_reopen(self):
        from types import MethodType
        gui, menu, component, parent=setup()
        self.native_screen_layout(gui,parent)
        self.assertTrue(all(isinstance(callback,MethodType) for callback in parent.onLayoutFinish))
        self.assertEqual(component.instance.size().height(),585)
        self.native_screen_layout(gui,parent)
        self.assertEqual(len(parent.onLayoutFinish),1)
        for callback in parent.onShow:callback()
        self.assertEqual(component.instance.size().height(),585)
    def test_reported_setup_original_has_partial_row_and_repair_removes_it(self):
        gui, menu, component, parent = setup()
        self.assertEqual(component.instance.partial_rows(), [(13,30)])
        self.assertTrue(component.applySkin(None,parent))
        self.assertEqual(component.instance.size().height(),585)
        self.assertEqual(component.instance.partial_rows(),[])
        self.assertEqual(component.instance.font,'Prive3;34')

    def test_native_navigation_visits_all_entries_and_returns_to_start(self):
        gui, menu, component, parent = setup(); component.applySkin(None,parent)
        visited = []
        for index in range(80):
            component.moveToIndex(index); visited.append(component.instance.index)
            self.assertEqual(component.instance.partial_rows(),[])
            self.assertLessEqual((index-component.instance.top+1)*45,585)
        self.assertEqual(visited,list(range(80)))
        component.pageDown(); self.assertEqual(component.instance.index,79)
        for unused in range(79): component.up()
        self.assertEqual(component.instance.index,0)

    def test_repeated_layout_does_not_shrink_and_uses_late_subclass_row_height(self):
        gui, menu, component, parent = setup()
        component.skinAttributes = [('size','1560,640'),('itemHeight','25')]
        component.applySkin(None,parent)
        self.assertEqual(component.instance.size().height(),625)
        component.instance.row = 40
        for callback in parent.onLayoutFinish: callback()
        self.assertEqual(component.instance.size().height(),640)
        for unused in range(3):
            for callback in parent.onShow: callback()
        self.assertEqual(component.instance.size().height(),640)
        self.assertEqual(len(parent.onLayoutFinish),1)

    def test_reapply_and_new_widget_restore_the_allocated_area(self):
        gui, menu, component, parent = setup(); component.applySkin(None,parent)
        component.skinAttributes = [('size','1560,720'),('itemHeight','45')]
        component.applySkin(None,parent); self.assertEqual(component.instance.size().height(),720)
        component.instance = Listbox(800,615,45)
        fit.fit(component,Listbox,Size); self.assertEqual(component.instance.size().height(),585)
        self.assertEqual(component.instance.size().width(),800)

    def test_scaled_actual_pixels_and_renderer_list_are_fitted(self):
        gui, menu, component, parent = setup(); parent.scale=((4,3),(4,3))
        del parent['config']; parent.renderer.append(component)
        component.applySkin(None,parent)
        self.assertEqual(component.instance.size().height(),780)
        self.assertEqual(component.instance.getItemHeight(),60)
        self.assertEqual(component.instance.size().width(),2080)

    def test_other_skins_grids_horizontal_and_spaced_layouts_are_preserved(self):
        gui, menu, component, parent = setup(active=False); component.applySkin(None,parent)
        self.assertEqual(component.instance.size().height(),615)
        for orientation in ('grid','horizontal'):
            gui, menu, component, parent = setup()
            component.skinAttributes.append(('listOrientation',orientation))
            component.applySkin(None,parent); self.assertEqual(component.instance.size().height(),615)
        gui, menu, component, parent = setup()
        component.skinAttributes.append(('itemSpacing','0,5'))
        component.applySkin(None,parent); self.assertEqual(component.instance.size().height(),615)

    def test_missing_geometry_and_short_viewport_do_not_break_older_backends(self):
        gui, menu, component, parent = setup()
        component.instance=SimpleNamespace(); self.assertFalse(fit.fit(component,Listbox,Size))
        component.instance=Listbox(height=20,row=45)
        self.assertFalse(fit.fit(component,Listbox,Size));self.assertEqual(component.instance.size().height(),20)

    def test_every_packaged_static_vertical_list_has_only_complete_rows(self):
        entries = list(static_lists())
        self.assertGreater(len(entries),100)
        for path, name, widget, width, height, row in entries:
            if row <= 0 or height < row: continue
            with self.subTest(path=path,screen=name,widget=widget.get('name',widget.get('source'))):
                component=SimpleNamespace(instance=Listbox(width,height,row),skinAttributes=list(widget.attrib.items()))
                fit.fit(component,Listbox,Size)
                self.assertEqual(component.instance.size().height()%row,0)
                self.assertLessEqual(component.instance.size().height(),height)
                self.assertEqual(component.instance.size().width(),width)

    def test_short_title_header_does_not_wrap_breadcrumb_into_half_a_line(self):
        gui, menu, component, parent=setup()
        title=object();parent['Title']=title
        header=gui();header.instance=Label();header.skinAttributes=[]
        header.source=SimpleNamespace(source=title)
        before=header.instance.text;header.applySkin(None,parent)
        self.assertEqual(header.instance.nowrap,1)
        self.assertEqual(header.instance.text,before)

    def test_multiline_titles_and_descriptions_remain_multiline(self):
        gui, menu, component, parent=setup();parent['Title']=object()
        header=gui();header.instance=Label(height=100,font=33);header.skinAttributes=[];header.source=parent['Title']
        header.applySkin(None,parent);self.assertEqual(header.instance.nowrap,0)
        description=gui();description.instance=Label();description.skinAttributes=[]
        description.source=object();description.applySkin(None,parent)
        self.assertEqual(description.instance.nowrap,0)

    def test_parent_scope_and_native_hook_order(self):
        tree=ast.parse((PLUGIN/'plugin.py').read_text())
        blocks=[node for node in tree.body if isinstance(node,ast.Try)]
        names=[(i,entry.module) for i,node in enumerate(blocks) for entry in node.body
               if isinstance(entry,ast.ImportFrom) and entry.module in ('warderListRows','warderConfigFonts')]
        self.assertEqual([name for i,name in names],['warderListRows','warderConfigFonts'])
        rowblock=blocks[names[0][0]]
        self.assertIn("config.skin.primary_skin.value == 'hd_glass17/skin.xml'",ast.unparse(rowblock))


if __name__ == '__main__': unittest.main(argv=[__file__]+rest)
