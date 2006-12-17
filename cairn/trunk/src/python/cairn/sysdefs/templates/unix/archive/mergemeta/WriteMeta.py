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
			raise cairn.Exception("Failed to open archive file", err)
		return


	def writeFile(self, sysdef, archive):
		try:
			meta = sysdef.readInfo.toStr()
			# 12 = len("__ARCHIVE__\n")
			print "offset", sysdef.info.getInt("archive/shar-offset")
			offset = int(sysdef.info.getInt("archive/shar-offset")) - 12
			if offset >= len(meta):
				archive.write(meta)
				archive.close()
			else:
				# Make room for the newer larger meta
				delta = len(meta) - offset
				
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file", err)
		return


	def run(self, sysdef):
		archive = self.openArchive(sysdef)
		self.writeFile(sysdef, archive)
		return True
