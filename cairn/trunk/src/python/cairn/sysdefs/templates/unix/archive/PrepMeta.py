"""templates.unix.copy.PrepMeta Module"""


import datetime

import cairn
from cairn import Options



def getClass():
	return PrepMeta()



class PrepMeta(object):

	def setDate(self, sysdef):
		sysdef.info.setChild("archive/date",
							 datetime.datetime.now().isoformat(' '))
		return

	def run(self, sysdef):
		self.setDate(sysdef)
		return True
