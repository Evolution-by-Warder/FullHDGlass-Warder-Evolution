#######################################################################
#
#    Concerter for Enigma2
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
import os
from Components.Converter.Converter import Converter
from time import localtime, strftime
from Components.Element import cached
from Components.Language import language
from Components.config import config
try:
	from Plugins.Extensions.setupGlass17.weaUtils import toLocale
except: pass

class g17ClockToText(Converter, object):
	DEFAULT = 0
	WITH_SECONDS = 1
	IN_MINUTES = 2
	DATE = 3
	FORMAT = 4
	AS_LENGTH = 5
	TIMESTAMP = 6

	def __init__(self, type):
		Converter.__init__(self, type)
		if type == "WithSeconds":
			self.type = self.WITH_SECONDS
		elif type == "InMinutes":
			self.type = self.IN_MINUTES
		elif type == "Date":
			self.type = self.DATE
		elif type == "AsLength":
			self.type = self.AS_LENGTH
		elif type == "Timestamp":	
			self.type = self.TIMESTAMP
		elif str(type).find("Format:") != -1:
			self.type = self.FORMAT
			self.fmt_string = type[7:]
		else:
			self.type = self.DEFAULT

	@cached
	def getText(self):
		time = self.source.time
		if time is None:
			return ""
		ign = True
		try:
			if not config.plugins.setupGlass17.par138.value:			
				ign = False
		except: pass
		if self.type == self.IN_MINUTES:
			return ({True:"%d min" % (time // 60), False:"%02d min" % (time // 60)}[ign])
		elif self.type == self.AS_LENGTH:
			return ({True:"%d" % (time // 60), False:"%02d" % (time // 60)}[ign]) + ":%02d" % time % 60
		elif self.type == self.TIMESTAMP:
			return str(time)		
		t = localtime(time)		
		if self.type == self.WITH_SECONDS:
			return ({True:"%2d" % t.tm_hour, False:"%02d" % t.tm_hour}[ign]) + ":%02d:%02d" % (t.tm_min, t.tm_sec)
		elif self.type == self.DEFAULT:
			return ({True:"%2d" % t.tm_hour, False:"%02d" % t.tm_hour}[ign]) + ":%02d" % t.tm_min
		elif self.type == self.DATE:
			try:
				s = toLocale(strftime("%A %B %d, %Y", t))
			except: 
				s =strftime("%A %B %d, %Y", t)
			return s
		elif self.type == self.FORMAT:
			try:
				if config.plugins.setupGlass17.par138.value:			
					self.fmt_string = self.fmt_string.replace("%H","%-H")
				if config.plugins.setupGlass17.par188.value:			
					self.fmt_string = self.fmt_string.replace("%d","%-d").replace("%m","%-m")
			except: pass
			spos = self.fmt_string.find('%')
			if spos > 0:
				s = str(self.fmt_string[:spos]+strftime(self.fmt_string[spos:], t))
			else:
				s = strftime(self.fmt_string, t)
			try:
				s = toLocale(s)
			except: pass
			return s
		else:
			return "???"

	text = property(getText)
