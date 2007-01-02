"""templates.unix.extract.meta.Replace Module"""



import os.path

import cairn
from cairn import Options
from cairn.sysdefs import SystemInfo



def getClass():
	return Replace()



class Replace(object):

	def run(self, sysdef):
		meta = Options.get("replace-meta")
		meta = os.path.abspath(meta)
		sysdef.readInfo = SystemInfo.readNew(meta)
		return True
