#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2020
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#######################################################################
from Components.VariableText import VariableText
from enigma import eLabel
from Components.Renderer.Renderer import Renderer
from os import popen, statvfs, path
from Components.config import config
try:
	from Plugins.Extensions.setupGlass17.txt import FREE,NA
except: 
	FREE = "free"    		
	NA = "N/A"
from Plugins.Extensions.setupGlass17.weaUtils import ISP38
if ISP38:
	from Plugins.Extensions.setupGlass17.py38 import DG
else:
	DG = unichr(176).encode("latin-1")
  			
class g17HDDstate(Renderer, VariableText):
	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)

	GUI_WIDGET = eLabel

	def changed(self, what):
		if self.instance and not self.suspended:
			hddState = NA
			hddSpace = NA
			hddType = "HDD"
			try:
				dev = config.plugins.setupGlass17.par140.value
				if dev != "None" and config.plugins.setupGlass17.par160.value:
					hddState = self.getTemp(dev)
					hddSpace = self.getSpace()
					hddType = config.plugins.setupGlass17.par182.value
			except:
				pass
			if hddState == NA and hddSpace == NA:
				self.text = " "
			else:
				self.text = "%s: %s %s, %s" % (hddType,hddState,DG+"C",hddSpace)
			
	def getSpace(self):
		try:              		
			temp = popen("df -h")
			for line in temp.readlines():
				parts = (line.replace('part1', ' ')).strip().split()
				totsp = len(parts) - 1
				if parts[totsp] == '/media/hdd':
					if ((parts[4].replace('%', '')).isdigit() or (parts[3].replace('%', '')).isdigit()):
						return parts[totsp-4] + "B  (" +  parts[totsp-2] + "B)  " + str(100 - int(parts[totsp-1].replace('%', ''))) + "%  " + FREE
		except OSError: pass
		return NA

	def getTemp(self,dev):
		tmp1 = 0                                                 
		w = ['smartctl -a %s | grep Temperature','/usr/bin/hdd_temp_hdg17 -q -n %s','hddtemp -n -q %s']
		for x in w:
			try:
				tta = x % dev
				temp = popen(tta).readline()
				if "smartctl" in tta:
					tmp1 = int((temp.strip().split("-")[1]).replace("\n","").replace("\t","").replace(" ",""))
				else:
					tmp1 = int(temp.strip().split(" ")[0])
			except: pass
			if tmp1 != 0:
				break
		if tmp1 == 0:
			return NA		
		return str(tmp1)	

	def onShow(self):
		self.suspended = False
		self.changed(None)

	def onHide(self):
		self.suspended = True

