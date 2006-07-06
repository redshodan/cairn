"""templates.unix.readmeta.ReadMeta Module"""



import os
import os.path

import cairn
from cairn import Options
from cairn.sysdefs import SystemInfo



def getClass():
	return ReadMeta()



class ReadMeta(object):

	def openFile(self, sysdef):
		filename = sysdef.info.get("archive/metafilename")
		try:
			archive = file(filename, "rb")
		except Exception, err:
			raise cairn.Exception("Unable to open meta file %s: %s" % \
								  (filename, err))
		return archive


	def run(self, sysdef):
		metafile = self.openFile(sysdef)
		sysdef.readInfo = SystemInfo.readNew(metafile)
		metafile.close()
		return True
