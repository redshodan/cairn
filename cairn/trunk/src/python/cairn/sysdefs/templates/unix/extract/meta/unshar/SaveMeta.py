"""templates.unix.extract.meta.unshar.SaveMeta"""


import os
import os.path

import cairn
from cairn import Options



def getClass():
	return SaveMeta()



class SaveMeta(object):

	def createFile(self, sysdef):
		return cairn.createFile(Options.get("unshar"), "w+", "metadata")


	def writeFile(self, sysdef, metaFile):
		try:
			metaFile.write(sysdef.readInfo.toStr(True))
			metaFile.close()
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file", err)
		return


	def run(self, sysdef):
		cairn.info("Extracting metadata")
		metaFile = self.createFile(sysdef)
		self.writeFile(sysdef, metaFile)
		return True
