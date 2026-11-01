#!/usr/bin/env python3
"""LCD4linux footer contract against its pinned native controller and real fonts."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from urllib.request import urlopen
import unittest
import xml.etree.ElementTree as ET
from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--upstream', type=Path)
args, remaining = parser.parse_known_args()
pin = json.loads((ROOT/'design/lcd4linux-footer/upstream.json').read_text())
raw = args.upstream.read_bytes() if args.upstream else urlopen(pin['url'], timeout=45).read(2 * 1024 * 1024)
text = raw.decode('utf-8').rstrip() + '\n'
assert hashlib.sha256(text.encode()).hexdigest() == pin['normalised_text_sha256']
start = text.index('class LCDdisplayConfig(')
end = text.index('\n\tdef layoutFinished', start)
controller = ast.parse(text[start:end]).body[0]
initial = next(n for n in controller.body if isinstance(n, ast.FunctionDef) and n.name == '__init__')
stop = next(i for i,n in enumerate(initial.body) if isinstance(n, ast.Assign) and any(isinstance(t,ast.Attribute) and t.attr=='session' for t in n.targets))
geometry = ast.FunctionDef(name='native_geometry',args=initial.args,body=initial.body[:stop],decorator_list=[],returns=None,type_comment=None)
ast.fix_missing_locations(geometry)
scope = {'getDesktop':lambda _:SimpleNamespace(size=lambda:SimpleNamespace(width=lambda:1920,height=lambda:1080)),
    'LCD4linux':SimpleNamespace(LCDType3=SimpleNamespace(value='00'))}
exec(compile(ast.Module(body=[geometry],type_ignores=[]),'native-lcd4linux-geometry','exec'),scope)
native = SimpleNamespace()
scope['native_geometry'](native,None)
original = ET.fromstring(native.skin)
skin = ET.parse(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').getroot()
screen = skin.find("screen[@name='LCDdisplayConfig']")
font = ImageFont.truetype(str(ROOT/'source/package-root/usr/share/fonts/prive7.ttf'),26)

def rectangle(node):
    x,y = map(int,node.get('position').split(','))
    w,h = map(int,node.get('size').split(','))
    return x,y,w,h

def wrap(value, width):
    lines=['']
    for word in value.split():
        test=(lines[-1]+' '+word).strip()
        if font.getlength(test)>width and lines[-1]:
            lines.append(word)
        else:
            lines[-1]=test
    return lines

class FooterTests(unittest.TestCase):
    def test_native_bitmap_menu_is_replaced_by_always_visible_caption(self):
        self.assertIsNotNone(original.find("ePixmap[@pixmap='skin_default/buttons/key_menu.png']"))
        self.assertIsNone(screen.find('ePixmap'))
        menu=screen.find("eLabel[@text='MENU']")
        self.assertNotIn('source',menu.attrib)
        self.assertNotIn('conditional',menu.attrib)
        self.assertIsNone(screen.find("widget[@source='key_menu']"))
        self.assertEqual(menu.get('foregroundColor'),'white')
        self.assertIn("self['key_menu'] = StaticText",ast.unparse(initial))
        self.assertIn("'menu': self.SetupMenu",ast.unparse(initial))

    def test_four_native_buttons_keep_names_and_live_text(self):
        for name,colour in (('key_red','red'),('key_green','green'),('key_yellow','yellow'),('key_blue','blue')):
            node=screen.find("widget[@name='%s']"%name)
            self.assertIsNotNone(original.find("widget[@name='%s']"%name))
            self.assertNotIn('source',node.attrib)
            self.assertNotIn('text',node.attrib)
            self.assertNotIn('render',node.attrib)
            self.assertEqual(node.get('foregroundColor'),colour)
            self.assertEqual(node.get('font'),'Prive3;26')
            self.assertEqual(node.get('transparent'),'1')

    def test_footer_bounds_clear_old_bottom_edge_and_do_not_overlap(self):
        nodes=[screen.find("widget[@name='%s']"%n) for n in ('key_red','key_green','key_yellow','key_blue')]
        nodes.append(screen.find("eLabel[@text='MENU']"))
        right=0
        for node in nodes:
            x,y,w,h=rectangle(node)
            self.assertGreaterEqual(x,right)
            self.assertLessEqual(x+w,910)
            self.assertLessEqual(y+h,940)
            self.assertLessEqual(50+30+y+h,1040)
            right=x+w
        self.assertEqual(screen.get('position'),'center,50')
        self.assertEqual(rectangle(screen.find("widget[@name='config']")),(0,0,910,800))

    def test_long_sk_cz_en_captions_and_mode_changes_fit_two_lines(self):
        samples=('Zrušiť','Uložiť','Reštart zobrazovačov','Nastaviť On >>','Nastaviť Media >>','Nastaviť Idle >>','Nastaviť Global >>',
            'Zrušit','Uložit','Restart displejů','Nastavit Media >>','Cancel','Save','Restart Displays','Set Global >>')
        for value in samples:
            lines=wrap(value,195)
            self.assertLessEqual(len(lines),2,value)
            self.assertTrue(all(font.getlength(line)<=195 for line in lines),value)
        menu_font=ImageFont.truetype(str(ROOT/'source/package-root/usr/share/fonts/prive7.ttf'),24)
        self.assertLessEqual(menu_font.getlength('MENU'),90)

    def test_preview_decoder_dimensions_positions_and_sources_stay_native(self):
        for name in ('LCD1','LCD2','LCD3'):
            self.assertEqual(rectangle(screen.find("widget[@name='%s']"%name)),rectangle(original.find("widget[@name='%s']"%name)))
        for name in ('LCD1text','LCD2text','LCD3text'):
            self.assertEqual(rectangle(screen.find("widget[@source='%s']"%name)),rectangle(original.find("widget[@source='%s']"%name)))
        for name in ('introduction','Version','About','LibUSB'):
            self.assertIsNotNone(screen.find("widget[@source='%s']"%name))

    def test_reversible_addition_keeps_every_previous_screen_byte_exact(self):
        ledger=json.loads((ROOT/'design/openatv81-compatibility/skin-edits.json').read_text())
        edit=next(e for e in ledger['edits'] if e['name']=='LCDdisplayConfig')
        self.assertEqual(edit['original_screen'],'')
        current=(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').read_text()
        self.assertEqual(current.count(edit['updated_screen']),1)
        self.assertNotIn('LCDdisplayConfig',current.replace(edit['updated_screen'],'',1))

if __name__=='__main__':
    unittest.main(argv=[__file__]+remaining)
