"""templates.unix.extract.meta.edit.PrepMetaForEdit Module"""



import os

import cairn
from cairn import Options



def getClass():
	return PrepMetaForEdit()



class PrepMetaForEdit(object):

	def openMeta(self, sysdef):
		meta = sysdef.info.get("archive/metafilename")
		try:
			metaFile = file(meta, "w+")
			return metaFile
		except Exception, err:
			raise cairn.Exception("Failed to open metadata file", err)
		return


	def writeMeta(self, sysdef, metaFile):
		try:
			sysdef.readInfo.saveToFile(metaFile, True)
			metaFile.close()
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file", err)
		return


	def run(self, sysdef):
		metaFile = self.openMeta(sysdef)
		self.writeMeta(sysdef, metaFile)
		return True
