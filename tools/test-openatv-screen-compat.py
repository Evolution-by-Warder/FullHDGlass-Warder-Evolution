"""Review native display contracts without executing image code or reading user data."""
from pathlib import Path
import argparse,ast,json,re,unittest,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--before',type=Path);parser.add_argument('--after',type=Path);args,rest=parser.parse_known_args()
SKIN=(ROOT/'source/package-root/usr/share/enigma2/hd_glass17/skin.xml').read_text();DOC=ET.fromstring(SKIN)
def screen(name):return DOC.find("screen[@name='%s']"%name)
def cls(root,module,name):return next(n for n in ast.parse((root/module).read_text()).body if isinstance(n,ast.ClassDef) and n.name==name)
def mandatory(node):
 result=set()
 for n in ast.walk(node):
  if isinstance(n,ast.Call):
   for k in n.keywords:
    if k.arg=='mandatoryWidgets':result.update(ast.literal_eval(k.value))
 return result

def active(widget,keys):
 conditional=widget.get('conditional');includes=widget.get('includes');excludes=widget.get('excludes')
 if conditional and not any(x in keys for x in conditional.split(',')):return False
 if includes and not any(x in keys for x in includes.split(',')):return False
 if excludes and any(x in keys for x in excludes.split(',')):return False
 return True

def widgets(name,keys):return [w for w in screen(name).findall('widget') if active(w,keys)]
class ScreenCompatTests(unittest.TestCase):
 def test_approved_pig_screen_is_byte_identical_and_only_registered_screens_change(self):
  record=json.loads((ROOT/'design/openatv-compatibility/skin-edits.json').read_text());text=SKIN
  cover_layout=ROOT/'design/radio-dab-cover-size/layout.json'
  if cover_layout.exists():
      for edit in json.loads(cover_layout.read_text())['edits']:
          self.assertEqual(text.count(edit['updated_screen']),1)
          text=text.replace(edit['updated_screen'],edit['original_screen'],1)
  layout=ROOT/'design/opkg-layout/layout.json'
  if layout.exists():
   for edit in json.loads(layout.read_text())['edits']:self.assertEqual(text.count(edit['updated_screen']),1);text=text.replace(edit['updated_screen'],edit['original_screen'],1)
  split=ROOT/'design/radio-dab-split/layout.json'
  if split.exists():
   for edit in json.loads(split.read_text())['edits']:self.assertEqual(text.count(edit['updated_screen']),1);text=text.replace(edit['updated_screen'],edit['original_screen'],1)
  for title in json.loads((ROOT/'design/radio-header/title.json').read_text())['edits']:self.assertEqual(text.count(title['updated_screen']),1);text=text.replace(title['updated_screen'],title['original_screen'],1)
  self.assertEqual({x['name'] for x in record['edits']},{'GraphicalEPG','PackageAction','ParentalControlSetup','ParentalControlChangePin','Setup','TextBox','NumberZapPicon'})
  for item in record['edits']:self.assertEqual(text.count(item['updated_screen']),1);text=text.replace(item['updated_screen'],item['original_screen'],1)
  import hashlib
  self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),record['before_skin_sha256'])
  block=lambda value:re.search(r'<screen\b[^>]*name="GraphicalEPGPIG"[\s\S]*?</screen>',value).group(0)
  self.assertEqual(block(text),block(SKIN))
 def test_native_no_pig_graph_colour_sources_are_rendered_as_sources(self):
  for colour in ('red','green','yellow','blue'):
   self.assertIsNotNone(screen('GraphicalEPG').find("widget[@source='key_%s'][@render='Label']"%colour))
   self.assertIsNone(screen('GraphicalEPG').find("widget[@name='key_%s']"%colour))
 def test_parental_setup_and_pin_keep_legacy_list_and_render_modern_mandatory_fields(self):
  for name in ('ParentalControlSetup','ParentalControlChangePin'):
   old={'config','key_red','key_green'};new=old|{'description','footnote','key_yellow','key_blue'}
   for keys,height in ((old,675),(new,555)):
    ws=widgets(name,keys);configs=[w for w in ws if w.get('name')=='config'];self.assertEqual(len(configs),1);self.assertEqual(int(configs[0].get('size').split(',')[1]),height)
    names={w.get('name') for w in ws};sources={w.get('source') for w in ws}
    if keys==new:self.assertTrue({'config','description','footnote'}<=names);self.assertTrue({'key_red','key_green','key_yellow','key_blue'}<=sources)
 def test_current_setup_required_components_and_package_action_keys_are_complete(self):
  if args.after:
   required=mandatory(cls(args.after,'Screens/Setup.py','Setup'));self.assertTrue(required<={w.get('name') for w in screen('Setup').findall('widget')})
   required_pin=required;self.assertTrue(required_pin<={w.get('name') for w in screen('ParentalControlChangePin').findall('widget')})
   package=cls(args.after,'Screens/PluginBrowser.py','PackageAction');keys=set()
   for n in ast.walk(package):
    if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='StaticText':
     for target in n.targets:
      if isinstance(target,ast.Subscript) and isinstance(target.slice,ast.Constant) and str(target.slice.value).startswith('key_'):keys.add(target.slice.value)
   self.assertTrue(keys<={w.get('source') for w in screen('PackageAction').findall('widget')},'OpenATV added/renamed a package action key; review the footer.')
 def test_new_package_search_and_menu_are_conditional_for_older_images(self):
  for key in ('key_blue','key_menu'):
   w=screen('PackageAction').find("widget[@source='%s']"%key);self.assertIsNotNone(w);self.assertEqual(w.get('conditional'),key);self.assertFalse(active(w,{'key_red','key_green','key_yellow'}))
 def test_textbox_preserves_old_full_height_and_shows_new_exit_caption(self):
  for keys,height in (({'text'},1080),({'text','key_red'},990)):
   ws=widgets('TextBox',keys);text=[w for w in ws if w.get('name')=='text'];self.assertEqual(len(text),1);self.assertEqual(int(text[0].get('size').split(',')[1]),height)
  red=screen('TextBox').find("widget[@source='key_red']");self.assertEqual(red.get('conditional'),'key_red')
 def test_native_swap_and_toast_use_their_verified_native_fallback_names(self):
  if not args.after:return
  swap=cls(args.after,'Screens/SwapManager.py','Swap');self.assertTrue(any(isinstance(n,ast.Assign) and any(isinstance(t,ast.Attribute) and t.attr=='skinName' for t in n.targets) and ast.literal_eval(n.value)==['SwapManagerSetup','Setup'] for n in ast.walk(swap)));self.assertIsNone(screen('SwapManagerSetup'));self.assertIsNotNone(screen('Setup').find("widget[@name='footnote']"))
  toast=cls(args.after,'Screens/Toast.py','ToastScreen');self.assertIn("['Toast']",ast.unparse(toast));self.assertIsNone(screen('Toast'))
  inline=next(n.value.value for n in toast.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='skin' for t in n.targets));names={w.get('name') for w in ET.fromstring(inline).findall('widget')};self.assertTrue(mandatory(toast)<=names)
 def test_parental_new_descriptions_and_footers_fit_without_overlap(self):
  for name in ('ParentalControlSetup','ParentalControlChangePin'):
   keys={'config','description','footnote','key_red','key_green','key_yellow','key_blue'};ws=widgets(name,keys);w,h=map(int,screen(name).get('size').split(','))
   for item in ws:
    x,y=map(int,item.get('position').split(','));width,height=map(int,item.get('size').split(','));self.assertLessEqual(x+width,w);self.assertLessEqual(y+height,h)
   byname={x.get('name'):x for x in ws if x.get('name')}
   for a,b in (('config','description'),('description','footnote')):
    self.assertLessEqual(sum(map(int,(byname[a].get('position').split(',')[1],byname[a].get('size').split(',')[1]))),int(byname[b].get('position').split(',')[1]))
if __name__=='__main__':unittest.main(argv=[__file__]+rest)
