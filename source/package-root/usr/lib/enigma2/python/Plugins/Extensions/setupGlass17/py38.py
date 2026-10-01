from Components.config import config, configfile
import six
import re
DG = '°' if six.PY3 else str('\xc2\xb0')
from html import entities as htmlentitydefs
iteritems = lambda d: d.items()
unichr = chr
    
def fixByteCode(w):
	w = (re.subn(r'<(script).*?</\1>(?s)', '', w)[0])
	w = (re.subn(r'<(style).*?</\1>(?s)', '', w)[0])
	entitydict = {}
	entities = re.finditer(r'&([:_A-Za-z][:_\-.A-Za-z"0-9]*);', w)
	for x in entities:
		key = x.group(0)
		if key not in entitydict:
			entitydict[key] = htmlentitydefs.name2codepoint[x.group(1)]
	entities = re.finditer('&#x([0-9A-Fa-f]+);', w)
	for x in entities:
		key = x.group(0)
		if key not in entitydict:
			entitydict[key] = "%d" % int(x.group(1), 16)
	entities = re.finditer(r'&#(\d+);', w)
	for x in entities:
		key = x.group(0)
		if key not in entitydict:
			entitydict[key] = x.group(1)
	if 'charset="utf-8"' in w or 'charset=utf-8' in w:
		for key, codepoint in six.iteritems(entitydict):
			cp = six.unichr(int(codepoint))
			w = w.replace(key, cp)
		return w
	for key, codepoint in six.iteritems(entitydict):
		cp = six.unichr(int(codepoint))
		w = w.replace(key, cp)
	return w.decode('latin-1')
        	