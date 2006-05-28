"""templates.unix.archive.readmeta.ExtractMeta Module"""



import cairn
from cairn import Options



def getClass():
	return ExtractMeta()



class ExtractMeta(object):

	def openFile(self, sysdef):
		filename = sysdef.info.get("archive/filename")
		try:
			archive = file(filename, "rb")
		except Exception, err:
			raise cairn.Exception("Unable to open archive file %s: %s" % \
								  (filename, err))
		return archive


	def isShar(self, sysdef, archive):
		line = archive.read(5)
		archive.close()
		if line.startswith("<?xml"):
			return True
		return False


	def run(self, sysdef):
		archive = self.openFile(sysdef)
		if self.isShar(sysdef, archive):
			sysdef.info.setChild("archive/shar", "True")
			sysdef.moduleList.insertAfterMe("archive.readmeta.ExtractMetaFromShar")
		else:
			sysdef.moduleList.insertAfterMe("archive.readmeta.ExtractMetaFromAR")
			sysdef.info.setChild("archive/shar", "False")
		return True
