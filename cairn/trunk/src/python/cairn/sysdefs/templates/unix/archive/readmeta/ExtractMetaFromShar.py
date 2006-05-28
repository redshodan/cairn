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
		metaEnd = 0
		for line in archive:
			metaEnd = pos
			pos = pos + len(line)
			if line.startswith("__ARCHIVE__"):
				break
		archive.seek(0)
		sysdef.info.setChild("archive/shar-offset", "%d" % (pos))
		return metaEnd


	def writeMeta(self, sysdef, archive, pos):
		metaFileName = os.path.join(sysdef.info.get("env/tmpdir"),
									"cairn-image.xml")
		cairn.verbose("Extracted metafile to: " + metaFileName)
		sysdef.info.setChild("archive/metafilename", metaFileName)
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
		return True
