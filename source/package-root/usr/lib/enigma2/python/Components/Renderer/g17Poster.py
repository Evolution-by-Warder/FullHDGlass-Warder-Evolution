# -*- coding: utf-8 -*-
#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2022
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
from enigma import ePixmap, eTimer, eActionMap
from Components.config import config
import os
import re
import json
from Plugins.Extensions.setupGlass17.weaUtils import netChck, ISP38
if ISP38:
	from urllib import request as urllibXX2
	from urllib.parse import quote_plus
	from Plugins.Extensions.setupGlass17.py38 import fixByteCode
else:
	import urllib2 as urllibXX2
	from urllib import quote_plus
ENA = False
try:
	from enigma import loadJPG
	if config.plugins.setupGlass17.par198.value:
		ENA = True
except: pass
	
PATH = "/media/cf"
try:
	PATH = config.plugins.setupGlass17.par39.value
except: pass
PATH = '%s/poster' % PATH
try:
	if not os.path.isdir(PATH):
		os.mkdir(PATH)
except: pass
FULLPATH = PATH + '/%s.jpg'

class g17Poster(Renderer):

	def __init__(self):
		Renderer.__init__(self)
		self.last = "Empty"
		self.__isInst = True
		self.__isHide = True
		self.__delayInitTimer = eTimer()
		try:
			self.__delayInitTimer_conn = self.__delayInitTimer.timeout.connect(self.searchPoster)
		except AttributeError:
			self.__delayInitTimer.timeout.get().append(self.searchPoster)
		self.enaExc = False
		try:
			self.enaExc = config.plugins.setupGlass17.par207.value
			if self.enaExc:
				self.RCkey = eActionMap.getInstance().bindAction('', -0x7FFFFFFF, self.doRC)
		except: pass
	GUI_WIDGET = ePixmap

	def doRC(self, key, flag):
		if key == 352 and flag == 3 and self.last != "Empty":
			try:
				dest = FULLPATH % self.image
				if os.path.isfile(dest):
					os.system("rm -rf " + dest)
					ff = PATH + '/_exceptions.txt'
					all = ""
					if os.path.isfile(ff):
						f = open(ff,"r")
						for i in f.readlines():
							if not self.image in i:
								all += i
						f.close()
					all += self.image + "\n"
					f = open(ff,"w")
					f.write(all)
					f.close()
					self.showPoster(None)
			except: pass
		return 0

	def changed(self, what):
		if self.instance and self.__isInst:
			self.instance.setScale(1)
			self.__isInst = False
			try:
				if config.plugins.setupGlass17.par161.value and config.plugins.setupGlass17.par203.value != "Empty":
					self.instance.setShowHideAnimation(config.plugins.setupGlass17.par203.value)
			except: pass
		event = self.source.event
		image = None
		if ENA and event is not None:
			try:
				name = event.getEventName()
				if name == self.last:
					return
				if self.__delayInitTimer.isActive():
					self.__delayInitTimer.stop()
				self.last = name
				p = r'((.*?)) \([T](\d+)\)'
				f = re.search(p,name)
				if f:
					name = f.group(1)
				image = name.replace(':',' ').replace('.',' ').replace('(',' ').replace(')',' ')
				if '«' in image and '»' in image:
					image = (image.split('«')[1]).split('»')[0]
				if '[' in image:
					image = image.split('[')[0]
				if ' -' in image:
					image = image.split(' -')[0]
				if '"' in image:
					image = (image.split('"')[1]).replace('"','')
				image = image.strip()
				image = re.sub(r'\s+', '+', image)
				dest = FULLPATH % image
				self.image = image
				if self.enaExc:
					ff = PATH + '/_exceptions.txt'
					if os.path.isfile(ff):
						f = open(ff,"r").read()
						if f.find(self.image) != -1:
							self.showPoster(None)
							return
				if os.path.isfile(dest):
					if os.path.getsize(dest) < 1000:
						os.system("rm -rf " + dest)
				if not os.path.isfile(dest):					
					self.showPoster(None)
					delay = 5
					try:
						delay = int(config.plugins.setupGlass17.par205.value)					
					except: pass					
					self.__delayInitTimer.startLongTimer(delay)
				else:
					self.showPoster(dest)
			except: pass
		elif image is None:
			self.showPoster(None)
			self.last = "Empty"		

	def showPoster(self, dest):
		try:
			if self.instance:
				if dest is not None:
					if self.image in dest:
						self.instance.setPixmap(loadJPG(dest))
						self.instance.show()
						self.__isHide = False
				elif not self.__isHide:
					self.instance.hide()
					self.__isHide = True
		except: pass

	def searchPoster(self):
		self.__delayInitTimer.stop()
		image = self.image
		self.dest = FULLPATH % image
		def chckUrl(d):
			mask = re.compile('<div.*?ipc-media--poster.*?<img.*?ipc-image.*?src="(http.*?)"', re.S)
			u = mask.search(d)
			if u and u.group(1).find("jpg") > 0:
				u = u.group(1)
				return u
			return None
		def downNow(w):
			try:
				f = open(self.dest,'wb')
				f.write(urllibXX2.urlopen(w).read())
				f.close()
				if os.path.isfile(self.dest):
					if os.path.getsize(self.dest) > 1000:
						return True
					else:
						os.system("rm -rf %s" % self.dest)
			except: pass
			return None
		imdb = "a"
		try:
			imdb = config.plugins.setupGlass17.par204.value
		except: pass
		if netChck(config.plugins.setupGlass17.par80.value):
			try:
				data = ""
				info = ""
				url = None
				if imdb in ("a","m") and url is None:
					for x in ("movie","tv","multi"):
						data = json.load(urllibXX2.urlopen("https://api.themoviedb.org/3/search/%s?api_key=3c3efcf47c3577558812bb9d64019d65&query=%s" % (x, quote_plus(image, safe='+'))))
						if 'results' in data and len(data['results']) != 0 and data['total_results'] != 0:
							ww = None
							if 'poster_path' in data['results'][0]:
								ww = data['results'][0]['poster_path'] 
							elif 'poster_path' in data['results'][0]['known_for'][0]:
								ww = data['results'][0]['known_for'][0]['poster_path']
							if ww:
								url = downNow("https://image.tmdb.org/t/p/w500%s" % ww)
							if url is not None:
								break
			except: pass
			try:
				if imdb in ("a","i") and url is None:
					infomask = re.compile(
						'<h1.*?class="TitleHeader__TitleText.*?>(?P<title>.*?)</h1>*'
						'(?:.*?>(?P<g_episodes>Episodes)<span.*?>(?P<episodes>.*?)</span>)?'
						r'(?:.*?class="OriginalTitle__OriginalTitleText.*?>(?P<g_originaltitle>.*?):\s.*?(?P<originaltitle>.*?)</div)?'
						r'(?:.*?<label for="browse-episodes-season".*?>.*?(?P<seasons>\d+)\s(?P<g_seasons>seasons?)</label>)?'
						'(?:.*?<span.*?>(?P<g_director>Directors?)(?:</span>|</a>).*?<div.*?<ul.*?>(?P<director>.*?)</ul>)?'
						'(?:.*?<span.*?>(?P<g_creator>Creators?)(?:</span>|</a>).*?<div.*?<ul.*?>(?P<creator>.*?)</ul>)?'
						'(?:.*?<span.*?>(?P<g_writer>Writers?)(?:</span>|</a>).*?<div.*?<ul.*?>(?P<writer>.*?)</ul>)?'
						'(?:.*?<a.*?>(?P<g_premiere>Release date)</a>.*?<div.*?<ul.*?>(?P<premiere>.*?)</ul>)?'
						'(?:.*?<span.*?>(?P<g_country>Countr.*?of origin)</span>.*?<div.*?<ul.*?>(?P<country>.*?)</ul>)?'
						'(?:.*?<a.*?>(?P<g_alternativ>Also known as)</a>.*?<div.*?<ul.*?>(?P<alternativ>.*?)</ul>)?'
						'(?:.*?<span.*?>(?P<g_runtime>Runtime)</span>.*?<div.*?>(?P<runtime>.*?)</div)?', re.S)
					htmlmask = re.compile('<.*?>')
					resultmask = re.compile(r'<tr class=\"findResult (?:odd|even)\">.*?<td class=\"result_text\"> <a href=\"/title/(tt\d{7,7})/.*?\"\s?>(.*?)</a>.*?</td>', re.S)
					data = urllibXX2.urlopen("https://www.imdb.com/find?ref_=nv_sr_fn&q=" + quote_plus(image, safe='+') + "&s=all").read()
					if ISP38:
						data = fixByteCode(str(data))
					info = infomask.search(data)
					if info:
						url = chckUrl(data)
					else:
						if not re.search('class="findHeader">No results found for', data):
							a = data.find("<table class=\"findList\">")
							b = data.find("</table>",a)
							all = data[a:b]
							all_res = resultmask.finditer(all)
							res = [(htmlmask.sub('',x.group(2)), x.group(1)) for x in all_res]
							if len(res) > 0:
								urld = "https://www.imdb.com/title/" + res[0][1] + "/"
								if ISP38:
									data = urllibXX2.urlopen(urld).read().decode('utf8', errors='ignore')
								else:
									data = urllibXX2.urlopen(urld).read()
								info = infomask.search(data)
								if info:
									url = chckUrl(data)
					if url:
						url = downNow(url)
				del data
				del info
			except: pass
		if not os.path.isfile(self.dest):
			self.dest = None
		self.showPoster(self.dest)
		
		
