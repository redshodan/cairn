"""templates.unix.archive.mergemeta.WriteMeta Module"""


import os
import os.path

import cairn
from cairn import Options



def getClass():
	return WriteMeta()



class WriteMeta(object):

	def openArchive(self, sysdef):
		filename = sysdef.info.get("archive/filename")
		try:
			archive = file(filename, "r+")
			return archive
		except Exception, err:
			raise cairn.Exception("Failed to open archive file: %s" % err)
		return


	def writeFile(self, sysdef, archive):
		try:
			sysdef.readInfo.saveToFile(archive, False)
			archive.close()
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file: %s" % err)
		return


	def run(self, sysdef):
		archive = self.openArchive(sysdef)
		self.writeFile(sysdef, archive)
		return True
