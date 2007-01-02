"""templates.unix.extract.meta.unshar.SaveMeta"""


import os
import os.path

import cairn
from cairn import Options



def getClass():
	return SaveMeta()



class SaveMeta(object):

	def createFile(self, sysdef):
		metaFileName = Options.get("unshar")
		try:
			path = re.split("/[^/]*$", metaFileName)
			os.makedirs(path[0], 0700)
		except:
			pass
		try:
			metaFile = file(metaFileName, "w+")
			return metaFile
		except Exception, err:
			raise cairn.Exception("Failed to open metadata file", err)
		return


	def writeFile(self, sysdef, metaFile):
		try:
			metaFile.write(sysdef.info.toStr())
			metaFile.close()
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file", err)
		return


	def run(self, sysdef):
		metaFile = self.createFile(sysdef)
		self.writeFile(sysdef, metaFile)
		return True
