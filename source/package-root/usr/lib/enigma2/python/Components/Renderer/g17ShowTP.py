#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2021
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
from Components.Renderer.Renderer import Renderer
from enigma import eLabel
from Components.VariableText import VariableText
from enigma import eServiceCenter, iServiceInformation, eDVBFrontendParametersSatellite, eDVBFrontendParametersCable, eDVBFrontendParametersTerrestrial
from xml.etree.cElementTree import parse
from Components.config import config
try:
	from Plugins.Extensions.setupGlass17.txt import NO_TP
	from Plugins.Extensions.setupGlass17.weaUtils import fixNameOf, chckIPTVprov, isSH
	if isSH() is not None:
		NO_TP = ""
except: NO_TP = 'TP info is not detected'
ENA_TT = False
try:
	from enigma import iDVBFrontend
	ENA_TT = True
except: pass
from Tools.Transponder import ConvertToHumanReadable
import os
from Plugins.Extensions.setupGlass17.weaUtils import ISP38
if ISP38:
	from Plugins.Extensions.setupGlass17.py38 import DG
else:
	DG = unichr(176).encode("latin-1")	

def chckE(w):
	if w != "x" and w != "":
		return w+"  "
	return ""
	
class g17ShowTP(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.ena = True
		try:
			self.ena = config.plugins.setupGlass17.par48.value
		except: pass
		if not self.ena:
			try:
				self.allSat = {}
				satellites = parse(config.plugins.setupGlass17.par141.value+"satellites.xml").getroot()
				if satellites is not None:
					for x in satellites.findall("sat"):
						name = x.get("name") or None
						position = x.get("position") or None
						if name is not None and position is not None:
							position = "%s.%s" % (position[:-1], position[-1:])
							if position.startswith("-"):
								position = "%sW" % position[1:]
							else:
								position = "%sE" % position
							if position.startswith("."):
								position = "0%s" % position
							if not ISP38:
								name = name.encode("utf-8")
							self.allSat[position] = str(name)
			except: pass
	GUI_WIDGET = eLabel

	def connect(self, source):
		Renderer.connect(self, source)
		self.changed((self.CHANGED_DEFAULT,))
		
	def changed(self, what):
		def convCH(what):
			fqT = ""
			try:
				fqT = int(((int(what) - 474) / 8) + 21)
				if fqT < 21 or fqT > 69:
					fqT = ""
				else:
					fqT = "MHz (CH %d) " % fqT						
			except: pass
			return fqT
		if self.instance:
			if what[0] == self.CHANGED_CLEAR:
				self.text = NO_TP
			else:
				serviceref = self.source.service
				info = eServiceCenter.getInstance().info(serviceref)
				if info and serviceref:
					sname = info.getInfoObject(serviceref, iServiceInformation.sTransponderData)
					fq = pol = fec = sr = orb = ""
					try:
						if sname:
							dataTP = ConvertToHumanReadable(sname)
						else:
							dataTP = { }
						orb = str(sname.get("tuner_type","None"))
						if ENA_TT and orb != "None":
							try:
								orb = {iDVBFrontend.feSatellite : "0",iDVBFrontend.feCable : "1",iDVBFrontend.feTerrestrial : "2",iDVBFrontend.feSatellite2 : "0",iDVBFrontend.feTerrestrial2 : "2"}[int(orb)]
							except: 
								try:
									orb = {iDVBFrontend.feSatellite : "0",iDVBFrontend.feCable : "1",iDVBFrontend.feTerrestrial : "2"}[int(orb)]
								except: pass
						if orb == "1":
							orb = "DVB-C"
						elif orb == "2" or "DVB-T" in orb:
							orb = "DVB-T"
							try:
								orb = {
											eDVBFrontendParametersTerrestrial.System_DVB_T : "DVB-T",
											eDVBFrontendParametersTerrestrial.System_DVB_T2 : "DVB-T2"
										}[sname.get("system", eDVBFrontendParametersTerrestrial.System_DVB_T)]
							except: pass
						if "frequency" in sname:
							fq = int(round(1.0 * int(sname["frequency"])/1000))
							if (fq > 9999 and fq < 99999 and "DVB-C" in orb) or fq > 99999:
								fq = int(round(1.0 * fq / 1000))
							fq = str(fq)
							if "DVB-T" in orb:
								fq += convCH(fq)							
						if "polarization" in sname:
							try:
								pol = {
									eDVBFrontendParametersSatellite.Polarisation_Horizontal : "H  ",
									eDVBFrontendParametersSatellite.Polarisation_Vertical : "V  ",
									eDVBFrontendParametersSatellite.Polarisation_CircularLeft : "CL  ",
									eDVBFrontendParametersSatellite.Polarisation_CircularRight : "CR  "}[sname["polarization"]]
							except: pass
						elif "bandwidth" in dataTP:
							pol = chckE(dataTP.get("bandwidth","x"))
						fec = dataTP.get("fec_inner","x")
						if fec == "x":
							fec = dataTP.get("code_rate_lp","x")
						if "symbol_rate" in sname:
							sr = "%s  " % (int(sname["symbol_rate"]) // 1000)
						if "orbital_position" in sname:	
							numSat = sname["orbital_position"]
							if numSat > 1800:
								numSat = str((float(3600 - numSat))/10.0)
								orb = numSat + DG + "W"
								numSat += "W"
							else:
								numSat = str((float(numSat))/10.0)
								orb = numSat + DG + "E"
								numSat += "E"
							if not self.ena:
								if numSat in self.allSat:
									orb = self.allSat.get(numSat)
								else:
									orb = "Sat on position: %s" % orb
					except:
						pass
					if fq != "":
						pls = ''
						if self.ena:
							if "pls_mode" in sname or "is_id" in sname or "pls_code" in sname:
								i = str(sname.get('is_id', 0))
								c = str(sname.get('pls_code', 0))
								m = str(sname.get('pls_mode', None))
								if not(m == 'None' or i == '-1' or i == '255' or i == '0' and c == '1'):
									if m.isdigit():
										try:
											m = {
												eDVBFrontendParametersSatellite.PLS_Root : "Root",
												eDVBFrontendParametersSatellite.PLS_Gold : "Gold",
												eDVBFrontendParametersSatellite.PLS_Combo : "Combo",
												eDVBFrontendParametersSatellite.PLS_Unknown : "U"}[sname["pls_mode"]]
										except: pass
									pls = ' MS:%s %s %s' % (i,c.replace('262143', ''),m.replace('U', ''))
							if "t2mi_plp_id" in sname:
								if sname.get('t2mi_plp_id') > -1:
									pls += ' T2-MI:%s %s' % (sname.get('t2mi_plp_id', 0), sname.get('t2mi_pid', 0))
						try:
							orb = orb.replace("E)",DG+"E)").replace("W)",DG+"W)")
						except: pass
						self.text = fq + " " + pol + chckE(fec) + sr + orb + pls
					else:
						try:
							sname = serviceref.toString()
							if sname is not None and sname != "":
								if sname.startswith("4097:0") or "3a//" in sname or "http" in sname:
									fq = "IPTV: " + fixNameOf(chckIPTVprov(sname))
									if "%3a//" in sname:
										fq = fq.replace(":","(" + (sname.split("%3a//")[0]).rsplit(":")[-1]	+ "):")							
						except: pass
						if fq != "":
							self.text = fq
						else:
							self.text = NO_TP
