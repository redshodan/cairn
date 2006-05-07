"""templates.unix.copy.write.RunArchiver Module"""



import os
import select
import shutil
import sys

import cairn
from cairn import Options
import cairn.sysdefs.templates.unix.archive.RunArchiver as tmpl



def getClass():
	return RunArchiver()



class RunArchiver(tmpl.RunArchiver):

	def prepare(self, sysdef):
		cairn.log("Creating archive")
		if sysdef.info.get("archive/shar"):
			archive = self.prepShar(sysdef)
		else:
			archive = self.prepArchive(sysdef)
		return archive


	def prepArchive(self, sysdef):
		fileName = sysdef.info.get("archive/filename")
		try:
			return os.open(fileName, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % \
								  (fileName, err))
		return


	def prepShar(self, sysdef):
		metaFileName = sysdef.info.get("archive/metafilename")
		fileName = sysdef.info.get("archive/filename")
		try:
			shutil.copyfile(metaFileName, fileName)
			archive = os.open(fileName, os.O_WRONLY | os.O_APPEND)
			os.write(archive, "\n__ARCHIVE__\n")
			os.fsync(archive)
			return archive
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % \
								  (fileName, err))
		return


	def direction(self):
		return self.OUT
