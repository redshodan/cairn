"""templates.unix.archive.readmeta.ExtractMetaFromShar Module"""


import os.path

import cairn
from cairn import Options



def getClass():
	return ExtractMetaFromShar()



class ExtractMetaFromShar(object):

	def openFile(self, sysdef):
		filename = sysdef.info.get("archive/filename")
		try:
			archive = file(filename, "rb")
		except Exception, err:
			raise cairn.Exception("Unable to open archive file %s: %s" % \
								  (filename, err))
		return archive


	def findMetaEnd(self, sysdef, archive):
		pos = 0
		for line in archive:
			if line.startswith("__ARCHIVE__"):
				break
			pos = pos + len(line)
		archive.seek(0)
		sysdef.info.set("archive/shar-offset", pos)
		return pos


	def writeMeta(self, sysdef, archive, pos):
		metaFileName = os.path.join(sysdef.info.get("env/tmpdir"),
									"cairn-image.xml")
		sysdef.info.set("archive/metafilename", metaFileName)
		try:
			metaFile = file(metaFileName, "w+b")
			xml = archive.read(pos)
			metaFile.write(xml)
			metaFile.close()
			archive.close()
		except Exception, err:
			raise cairn.Exception("Unable to write meta file %s: %s" % \
								  (metaFileName, err))
		return


	def run(self, sysdef):
		archive = self.openFile(sysdef)
		pos = self.findMetaEnd(sysdef, archive)
		self.writeMeta(sysdef, archive, pos)
		return true
