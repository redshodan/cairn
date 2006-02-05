"""templates.unix.copy.WriteMeta Module"""


import os
import os.path

import cairn
from cairn import Options



def getClass():
	return WriteMeta()



class WriteMeta(object):

	def createFile(self, sysdef):
		metaFileName = sysdef.info.get("archive/metafilename")
		try:
			path = os.path.dirname(metaFileName)
			os.mkdirs(path[0])
		except:
			pass
		try:
			metaFile = file(metaFileName, "w+")
			return metaFile
		except Exception, err:
			raise cairn.Exception("Failed to open metadata file: " + err)
		return


	def writeFile(self, sysdef, metaFile):
		try:
			sysdef.info.saveToFile(metaFile)
			metaFile.close()
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file: " + err)
		return


	def run(self, sysdef):
		metaFile = self.createFile(sysdef)
		self.writeFile(sysdef, metaFile)
		return True
