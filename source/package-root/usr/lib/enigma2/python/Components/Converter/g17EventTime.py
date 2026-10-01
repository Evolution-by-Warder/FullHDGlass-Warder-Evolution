from Components.Converter.Converter import Converter
from Components.Converter.Poll import Poll
from time import time, localtime
from Components.Element import cached, ElementError
from Components.config import config

class g17EventTime(Poll, Converter, object):
	REMAINING = 0
	STARTTIME = 1
	DURATION = 2
	ENDTIME = 3
    	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "Remaining":
			self.type = self.REMAINING
			self.poll_interval = 60000
			self.poll_enabled = True
		elif type == "StartTime":
			self.type = self.STARTTIME
		elif type == "Duration":
			self.type = self.DURATION
		elif type == "EndTime":
			self.type = self.ENDTIME
		else:
			raise ElementError("'%s' is not <Remaining> for g17EventTime converter" % type)

	@cached
	def getText(self):
		def conv_to_default(what):
			t = localtime(what)
			return ({True:"%2d" % t.tm_hour, False:"%02d" % t.tm_hour}[ign]) + ":%02d" % t.tm_min
		def conv_to_min(what):
			return ({True:"%d min" % (what / 60), False:"%02d min" % (what / 60)}[ign])
		event = self.source.event
		if event is None:
			return "--"			
		ign = True
		try:
			if not config.plugins.setupGlass17.par138.value:			
				ign = False
		except: pass
		if self.type == self.REMAINING:
			now = int(time())
			start = event.getBeginTime()
			duration = event.getDuration()
			end = start + duration
			if start <= now <= end:
				return conv_to_min(end - now) 
		elif self.type == self.STARTTIME:			
			return conv_to_default(event.getBeginTime())
		elif self.type == self.DURATION:
			return conv_to_min(event.getDuration())
		elif self.type == self.ENDTIME:
			return conv_to_default(event.getBeginTime() + event.getDuration())
		return "--"	

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)
