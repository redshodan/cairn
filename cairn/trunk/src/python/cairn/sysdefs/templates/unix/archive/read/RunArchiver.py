"""templates.unix.read.RunArchiver Module"""



import os
import select
import shutil
import sys

import cairn
from cairn import Options
from cairn.sysdefs.templates.unix.misc import Process



def getClass():
	return CreateArchive()



class RunArchiver(object):

	def prepare(self, sysdef):
		fileName = sysdef.info.get("archive/filename")
		try:
			return os.open(fileName, os.O_RDONLY)
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % \
								  (fileName, err))
		return


	def direction(self):
		return self.IN
