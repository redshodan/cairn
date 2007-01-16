"""templates.unix.meta.Replace Module"""



import os.path

import cairn
from cairn import Options
from cairn.sysdefs import SystemInfo



def getClass():
	return Replace()



class Replace(object):

	def findFilename(self, sysdef):
		if Options.getExtraOpts():
			return Options.getExtraOpts()[0]
		else:
			raise cairn.UserEx("Missing meta filename")


	def run(self, sysdef):
		meta = self.findFilename(sysdef)
		meta = os.path.abspath(meta)
		sysdef.readInfo = SystemInfo.readNew(meta)
		return True
