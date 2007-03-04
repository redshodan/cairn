"""templates.unix.meta.unshar.SaveMeta"""


import os
import os.path
import re

import cairn
from cairn import Options



def getClass():
	return SaveMeta()



class SaveMeta(object):

	def findFilename(self, sysdef):
		if Options.getExtraOpts():
			return Options.getExtraOpts()[0]
		else:
			filename = Options.get("filename")
			if re.match("\.cimg$", filename):
				return re.sub("\.cimg$", ".meta", filename)
			else:
				return filename + ".meta"


	def createFile(self, sysdef, filename):
		return cairn.createFile(filename, "w+", "metadata")


	def writeFile(self, sysdef, metaFile):
		try:
			metaFile.write(sysdef.readInfo.toStr(True))
			metaFile.close()
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file", err)
		return


	def run(self, sysdef):
		filename = self.findFilename(sysdef)
		cairn.info("Extracting metadata to: %s" % filename)
		metaFile = self.createFile(sysdef, filename)
		self.writeFile(sysdef, metaFile)
		return True
