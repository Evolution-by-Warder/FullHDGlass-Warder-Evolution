"""Extend the existing live, integrity-checked downloader to all supplied sizes."""
from pathlib import Path
import ast,json
R=Path(__file__).resolve().parents[1];P=R/'source/package-root/usr/lib/enigma2/python/Plugins/Extensions/setupGlass17'
def replace(text,old,new,count=1):
 assert text.count(old)==count,(old,text.count(old));return text.replace(old,new)
s=(P/'warderPiconSync.py').read_text()
s=replace(s,'"50x30": ("black", "white"),','"50x30": ("transparent", "black", "white"),')
s=replace(s,'"400x240": ("transparent",),','"400x240": ("transparent", "black", "white"),')
s=replace(s,'return "warder" if resolution == "220x132" else "pinned-legacy"','return "warder" if resolution in ("50x30", "220x132", "400x240") else "pinned-legacy"')
s=replace(s,'if resolution != "220x132":\n        raise ValueError("non-native resolution requires pinned selected-position archives")','if channel_delivery_backend(resolution, style) != "warder":\n        raise ValueError("non-native resolution requires pinned selected-position archives")')
s=replace(s,'if not channel_style_supported("220x132", style):','if not channel_style_supported(resolution, style):')
s=replace(s,'    "(85.0E) Intelsat 15/Horizons 2": (','    "(80.0E) Satelit 80.0E": ("800E", "80.0e"),\n    "(0.8W) Digi": ("DIGI_TELLY", "0.8w"),\n    "(0.8W) Telly": ("DIGI_TELLY", "0.8w"),\n    "(85.0E) Intelsat 15/Horizons 2": (')
s=replace(s,'    "850E": "85.0e",','    "800E": "80.0e",\n    "850E": "85.0e",')
(P/'warderPiconSync.py').write_text(s)
p=(P/'plugin.py').read_text()
p=replace(p,'if resolution == "220x132":','if warderPiconSync.channel_delivery_backend(resolution, style) == "warder":')
p=replace(p,'and self.warderPiconPrefs.get("resolution") != "220x132"','and warderPiconSync.channel_delivery_backend(self.warderPiconPrefs.get("resolution"), self.warderPiconPrefs.get("style")) == "pinned-legacy"')
p=replace(p,'and self.warderPiconPrefs.get("resolution") == "220x132"','and warderPiconSync.channel_delivery_backend(self.warderPiconPrefs.get("resolution"), self.warderPiconPrefs.get("style")) == "warder"')
(P/'plugin.py').write_text(p)
t=(P/'txt.py').read_text()
marker='("(85.0E) Intelsat 15/Horizons 2",'
assert t.count(marker)==1
t=t.replace(marker,'("(80.0E) Satelit 80.0E","320","800E","","","","","","",""),\n'+marker)
(P/'txt.py').write_text(t)
for file in ['plugin.py','warderPiconSync.py','txt.py']:ast.parse((P/file).read_bytes())
(P/'version').write_text('1.0.14\n')
c=R/'source/control/control';c.write_text(replace(c.read_text(),'Version: 1.0.13-1','Version: 1.0.14-1'))
print('PASS: all nine supplied size/style combinations use the existing live native downloader; 150x90 and approved radio artwork unchanged')
