"""Check the actual OpenATV widget contract and native key asset geometry."""
import argparse,ast,hashlib,io,json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
PAYLOAD=ROOT/'source/package-root'
RECORD=json.loads((ROOT/'design/virtual-keyboard/compatibility.json').read_text())
SKIN=PAYLOAD/'usr/share/enigma2/hd_glass17/skin.xml'
DOCUMENT=ET.fromstring(SKIN.read_bytes())
SCREEN=DOCUMENT.find("screen[@name='VirtualKeyboard']")
parser=argparse.ArgumentParser();parser.add_argument('--upstream',required=True,type=Path);parser.add_argument('--latest',type=Path);args,remaining=parser.parse_known_args()
UPSTREAM=args.upstream.read_bytes()

class KeyboardTests(unittest.TestCase):
    def test_latest_upstream_additions_or_renames_require_explicit_skin_review(self):
        raw=args.latest.read_bytes() if args.latest else UPSTREAM
        cls=next(n for n in ast.parse(raw).body if isinstance(n,ast.ClassDef) and n.name=='VirtualKeyboard')
        init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
        contract={}
        for node in ast.walk(init):
            if isinstance(node,ast.Assign) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id in ('Label','Input','VirtualKeyboardList','StaticText'):
                for target in node.targets:
                    if isinstance(target,ast.Subscript) and isinstance(target.value,ast.Name) and target.value.id=='self':contract[ast.literal_eval(target.slice)]=node.value.func.id
        self.assertEqual(contract,RECORD['upstream_component_contract'],'OpenATV display contract changed: review the skin before publishing')
    def test_current_controller_fields_are_all_rendered_without_legacy_names(self):
        self.assertEqual(hashlib.sha256(UPSTREAM).hexdigest(),RECORD['upstream_sha256'])
        cls=next(n for n in ast.parse(UPSTREAM).body if isinstance(n,ast.ClassDef) and n.name=='VirtualKeyboard')
        init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
        names=set()
        for n in ast.walk(init):
            if isinstance(n,ast.Assign):
                for t in n.targets:
                    if isinstance(t,ast.Subscript) and isinstance(t.value,ast.Name) and t.value.id=='self':
                        try:names.add(ast.literal_eval(t.slice))
                        except (ValueError,TypeError):pass
        widgets={w.get('name') for w in SCREEN.findall('widget') if w.get('name')}
        sources={w.get('source') for w in SCREEN.findall('widget') if w.get('source')}
        self.assertTrue(widgets|sources <= names)
        self.assertTrue(set(RECORD['required_widget_names']) <= widgets)
        self.assertTrue(set(RECORD['required_sources']) <= sources)
        self.assertNotIn('header',widgets);self.assertNotIn('country',sources)

    def test_prompt_uses_the_plugin_label_for_user_name_and_password(self):
        cls=next(n for n in ast.parse(UPSTREAM).body if isinstance(n,ast.ClassDef) and n.name=='VirtualKeyboard')
        init=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__init__')
        statement=next(n for n in init.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Subscript) and ast.literal_eval(t.slice)=='prompt' for t in n.targets if isinstance(t,ast.Subscript)))
        for prompt in ('Účet – meno (písmená, čísla, _ a -)','Účet – heslo'):
            self.assertEqual(ast.dump(statement.value),ast.dump(ast.parse('Label(prompt)',mode='eval').body))
            scope={'self':{},'Label':lambda text:text,'prompt':prompt}
            exec(compile(ast.Module(body=[statement],type_ignores=[]),'upstream-prompt','exec'),scope)
            self.assertEqual(scope['self']['prompt'],prompt)
        field=SCREEN.find("widget[@name='prompt']")
        self.assertNotEqual(field.get('noWrap'),'1')
        self.assertGreaterEqual(int(field.get('size').split(',')[1]),100)
        self.assertEqual(SCREEN.find("widget[@name='text']").get('name'),'text')

    def test_cells_rows_and_existing_icon_dimensions_match(self):
        fonts={n.get('name'):n for n in DOCUMENT.findall('.//fonts/alias')}
        self.assertEqual(fonts['VirtualKeyboard'].get('height'),'67')
        keys=PAYLOAD/'usr/share/enigma2/hd_glass17/buttons'
        for kind in ('bg','sel','red','green','yellow','blue'):
            with Image.open(keys/('vkey_'+kind+'.png')) as original:
                pieces=[]
                for label in ('l','m','r'):
                    with Image.open(keys/('vkey_'+kind+'_'+label+'.png')) as part:pieces.append(part.convert('RGBA'))
                self.assertEqual([p.height for p in pieces],[67]*3)
                self.assertEqual(sum(p.width for p in pieces),67)
                joined=Image.new('RGBA',(67,67));x=0
                for part in pieces:joined.paste(part,(x,0));x+=part.width
                self.assertEqual(joined.tobytes(),original.convert('RGBA').tobytes())
        self.assertEqual(SCREEN.find("widget[@name='list']").get('size'),'938,335')

    def test_every_widget_fits_and_prompt_input_grid_and_footer_do_not_overlap(self):
        width,height=map(int,SCREEN.get('size').split(','))
        for widget in SCREEN:
            x,y=map(int,widget.get('position').split(','));w,h=map(int,widget.get('size').split(','))
            self.assertGreaterEqual(min(x,y),0);self.assertLessEqual(x+w,width);self.assertLessEqual(y+h,height)
        fields=[SCREEN.find("widget[@name='%s']"%name) for name in ('prompt','text','mode','list','locale')]
        for a,b in zip(fields,fields[1:]):
            self.assertLessEqual(int(a.get('position').split(',')[1])+int(a.get('size').split(',')[1]),int(b.get('position').split(',')[1]))

    def test_only_the_modern_screen_changes_and_legacy_screen_is_preserved(self):
        raw=SKIN.read_text()
        from openatv81_skin import revert_skin
        raw=revert_skin(ROOT,raw)
        cover_layout=ROOT/'design/radio-dab-cover-size/layout.json'
        if cover_layout.exists():
            for edit in json.loads(cover_layout.read_text())['edits']:
                self.assertEqual(raw.count(edit['updated_screen']),1)
                raw=raw.replace(edit['updated_screen'],edit['original_screen'],1)
        layout=ROOT/'design/opkg-layout/layout.json'
        if layout.exists():
            for edit in json.loads(layout.read_text())['edits']:
                self.assertEqual(raw.count(edit['updated_screen']),1)
                raw=raw.replace(edit['updated_screen'],edit['original_screen'],1)
        self.assertEqual(raw.count(RECORD['updated_screen']),1)
        split_edits=ROOT/'design/radio-dab-split/layout.json'
        if split_edits.exists():
            for edit in json.loads(split_edits.read_text())['edits']:
                self.assertEqual(raw.count(edit['updated_screen']),1)
                raw=raw.replace(edit['updated_screen'],edit['original_screen'],1)
        title_edits=ROOT/'design/radio-header/title.json'
        if title_edits.exists():
            for edit in json.loads(title_edits.read_text())['edits']:
                self.assertEqual(raw.count(edit['updated_screen']),1)
                raw=raw.replace(edit['updated_screen'],edit['original_screen'],1)
        compatibility_edits=ROOT/'design/openatv-compatibility/skin-edits.json'
        if compatibility_edits.exists():
            for edit in json.loads(compatibility_edits.read_text())['edits']:
                self.assertEqual(raw.count(edit['updated_screen']),1)
                raw=raw.replace(edit['updated_screen'],edit['original_screen'],1)
        restored=raw.replace(RECORD['updated_screen'],RECORD['original_screen'],1).encode()
        self.assertEqual(hashlib.sha256(restored).hexdigest(),RECORD['original_skin_sha256'])
        original=ET.fromstring(restored)
        self.assertEqual(ET.tostring(DOCUMENT.find("screen[@name='VirtualKeyBoard']")),ET.tostring(original.find("screen[@name='VirtualKeyBoard']")))

if __name__=='__main__':unittest.main(argv=[__file__]+remaining)
