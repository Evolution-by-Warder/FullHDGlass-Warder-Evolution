from Components.MenuList import MenuList
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from enigma import eListboxPythonMultiContent, eListbox, gFont, RT_HALIGN_LEFT
from Tools.LoadPixmap import LoadPixmap

selectionpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/icons/selectioncross.png"))

def SelectionEntryComponent(description, value, index, selected, pict):
	res = [
		(description, value, index, selected, pict),
		(eListboxPythonMultiContent.TYPE_TEXT, 140, 12, 900, 45, 0, RT_HALIGN_LEFT, description),
		(eListboxPythonMultiContent.TYPE_PIXMAP_ALPHABLEND, 55, 8, 75, 45, LoadPixmap(pict))
	]
	if selected:
		res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 0, 8, 45, 45, selectionpng))
	return res

class SelectionList(MenuList):
	def __init__(self, list = None, enableWrapAround = False):
		MenuList.__init__(self, list or [], enableWrapAround, content = eListboxPythonMultiContent)
		self.l.setFont(0, gFont("Prive4", 36))
		self.l.setItemHeight(60)

	def addSelection(self, description, value, index, selected, pict):
		self.list.append(SelectionEntryComponent(description, value, index, selected, pict))
		self.setList(self.list)

	def toggleSelection(self):
		idx = self.getSelectedIndex()
		item = self.list[idx][0]
		self.list[idx] = SelectionEntryComponent(item[0], item[1], item[2], not item[3], item[4])
		self.setList(self.list)

	def getSelectionsList(self):
		return [ (item[0][0], item[0][1], item[0][2]) for item in self.list if item[0][3] ]

