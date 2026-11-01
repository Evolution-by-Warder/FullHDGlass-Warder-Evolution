#!/usr/bin/env python3
"""Real native menu-hint transitions, list capacity and FullHDGlass text bounds."""
import argparse, ast, hashlib, json, textwrap, unittest
from pathlib import Path
from types import SimpleNamespace
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from PIL import ImageFont, Image
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(add_help=False)
parser.add_argument('--upstream',type=Path)
args,remaining=parser.parse_known_args()
pin=json.loads((ROOT/'design/quick-menu/upstream.json').read_text())
sources={}
for item in pin['files']:
    raw=(args.upstream/item['local_file']).read_bytes() if args.upstream else urlopen('https://raw.githubusercontent.com/openatv/enigma2/'+pin['commit']+'/'+item['path'],timeout=45).read(1024*1024)
    text=raw.decode().rstrip()+'\n'
    assert hashlib.sha256(text.encode()).hexdigest()==item['sha256']
    sources[item['local_file']]=text
def method(source,name):
    start=source.index('\tdef '+name+'(')
    end=source.find('\n\tdef ',start+1)
    return ast.parse(textwrap.dedent(source[start:end if end>=0 else None])).body[0]
def executable(node,scope):
    env=dict(scope)
    exec(compile(ast.Module(body=[node],type_ignores=[]),'native-menu-method','exec'),env)
    return env[node.name]
skin=ET.parse(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').getroot()
quick=skin.find("screen[@name='QuickMenu']")
lcd=skin.find("screen[@name='LCDdisplayConfig']")
ledger=json.loads((ROOT/'design/openatv81-compatibility/skin-edits.json').read_text())
old=ET.fromstring(next(e for e in ledger['edits'] if e['name']=='QuickMenu')['original_screen'])
class NativeList:
    def setList(self,value): self.value=value
class Hint:
    def setText(self,value): self.text=value
class Entry:
    def isReadOnly(self): return False
class Selection(Entry): pass
class Integer(Entry): pass
class Sequence(Entry): pass
class Text(Entry): pass
class MacText(Text): pass
class Number(Text): pass
class QuickTests(unittest.TestCase):
    def test_native_config_list_changes_hint_but_lcd_menu_stays_fixed(self):
        helper=executable(method(sources['native-configlist-menu.py'],'handleInputHelpers'),{
            '_':lambda x:x,'ConfigSelection':Selection,'ConfigInteger':Integer,'ConfigSequence':Sequence,
            'ConfigText':Text,'ConfigMACText':MacText,'ConfigNumber':Number})
        actions=SimpleNamespace(setEnabledAction=lambda *a:None,setEnabled=lambda *a:None)
        owner={n:actions for n in ('configActions','navigationActions','menuConfigActions','charConfigActions','editConfigActions')}
        hint=Hint();owner['key_menu']=hint
        values=[]
        for entry in (Selection(),Entry(),Integer(),Selection()):
            owner['config']=SimpleNamespace(getCurrent=lambda full=False,e=entry:('value',e))
            helper(owner);values.append(hint.text)
        self.assertEqual(values,['MENU','','','MENU'])
        self.assertIsNone(lcd.find("widget[@source='key_menu']"))
        self.assertIsNotNone(lcd.find("eLabel[@text='MENU']"))

    def test_native_ten_categories_and_nine_software_items_fit(self):
        source=sources['native-quickmenu.py']
        owner={'mainlist':NativeList()}
        class Owner(dict): pass
        owner=Owner(owner)
        env={'_':lambda x:x,'BoxInfo':SimpleNamespace(getItem=lambda key:True),
            'LoadPixmap':lambda *a:None,'resolveFilename':lambda *a:'icon','SCOPE_SKIN':0}
        executable(method(source,'showMainMenu'),env)(owner)
        owner.quickSubMenuEntryComponent=lambda *a,**k:a
        owner.setSubList=lambda:None
        executable(method(source,'subMenuSoftware'),{'_':lambda x:x})(owner)
        self.assertEqual(len(owner.mainList),10)
        self.assertEqual(len(owner.subList),9)
        for name,count in (('mainlist',len(owner.mainList)),('sublist',len(owner.subList))):
            previous=old.find("widget[@source='%s']"%name)
            node=quick.find("widget[@source='%s']"%name)
            self.assertEqual(int(previous.get('size').split(',')[1])//int(previous.get('itemHeight')),8)
            self.assertGreaterEqual(int(node.get('size').split(',')[1])//int(node.get('itemHeight')),count)

    def test_borderless_screen_header_lists_help_and_footer_do_not_overlap(self):
        self.assertEqual(quick.get('flags'),'wfNoBorder')
        self.assertEqual(quick.get('position'),'0,0')
        self.assertEqual(quick.get('size'),'1920,1080')
        for node in list(quick):
            if not node.get('position'):continue
            x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
            self.assertTrue(0<=x<x+w<=1920 and 0<=y<y+h<=1080,node.attrib)
        for name in ('mainlist','sublist'):
            node=quick.find("widget[@source='%s']"%name)
            y=int(node.get('position').split(',')[1]);h=int(node.get('size').split(',')[1])
            self.assertEqual(y+h,860)
        self.assertEqual(quick.find("widget[@name='description']").get('position'),'80,875')

    def test_long_sk_titles_and_descriptions_fit_actual_fonts(self):
        path=ROOT/'source/package-root/usr/share/fonts/prive7.ttf'
        title=ImageFont.truetype(str(path),28);body=ImageFont.truetype(str(path),22)
        for value in ('Vybrať súbory vylúčené zo zálohovania','Vybrať ďalšie súbory na zálohovanie','Zobraziť predvolené záložné súbory','Nastavenia Správcu softvéru'):
            self.assertLessEqual(title.getlength(value),830,value)
        for value in ('Výber súborov, ktoré sa nemajú zálohovať','Aktualizácia/zálohovanie/obnova prijímača','Spravovanie online aktualizačných súborov'):
            self.assertLessEqual(body.getlength(value),755,value)

    def test_native_sources_template_indices_and_coloured_keys_are_preserved(self):
        for name in ('mainlist','sublist','key_red','key_green','key_yellow','key_blue'):
            self.assertIsNotNone(quick.find("widget[@source='%s']"%name))
        for name in ('mainlist','sublist'):
            before=old.find("widget[@source='%s']"%name)
            after=quick.find("widget[@source='%s']"%name)
            self.assertEqual([n.get('index') for n in before.iter() if n.get('index')],[n.get('index') for n in after.iter() if n.get('index')])
            self.assertEqual(after.get('scrollbarMode'),'showOnDemand')
            self.assertEqual(after.find('templates/template').get('itemHeight'),after.get('itemHeight'))

    def test_tv_colour_rules_use_opaque_solid_pngs_below_captions(self):
        expected={'red':(255,0,0,255),'green':(29,215,31,255),'yellow':(253,234,0,255),'blue':(0,19,255,255)}
        for (name,rgba),x in zip(expected.items(),(80,534,988,1443)):
            relative='hd_glass17/videodb/'+name+'.png'
            node=quick.find("ePixmap[@pixmap='%s']"%relative)
            self.assertIsNotNone(node)
            self.assertEqual(node.get('position'),str(x)+',1019')
            self.assertEqual(node.get('size'),'397,4')
            self.assertEqual(node.get('scale'),'1')
            self.assertEqual(node.get('alphatest'),'off')
            pixels=Image.open(ROOT/'source/package-root/usr/share/enigma2'/relative).convert('RGBA')
            self.assertEqual(set(pixels.getdata()),{rgba})
            self.assertLessEqual(1019+4,1080)
        self.assertFalse(any(n.get('position','').endswith(',1019') for n in quick.findall('eLabel')))

if __name__=='__main__':
    unittest.main(argv=[__file__]+remaining)
