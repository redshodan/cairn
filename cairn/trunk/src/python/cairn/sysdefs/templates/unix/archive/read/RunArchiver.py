"""templates.unix.archive.read.RunArchiver Module"""



import os
import select
import shutil
import sys

import cairn
from cairn import Options
import cairn.sysdefs.templates.unix.archive.RunArchiver as tmpl
from cairn.sysdefs.templates.unix.misc import Process



def getClass():
	return RunArchiver()



class RunArchiver(tmpl.RunArchiver):

	def prepare(self, sysdef):
		sysdef.info.setChild("archive/estimated-size",
							 sysdef.readInfo.get("archive/size"))
		fileName = sysdef.info.get("archive/filename")
		try:
			fd = os.open(fileName, os.O_RDONLY)
			if sysdef.readInfo.get("archive/shar"):
				os.lseek(fd, long(sysdef.readInfo.get("archive/shar-offset")), 0)
			return fd
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % \
								  (fileName, err))
		return -1


	def direction(self):
		return self.IN
