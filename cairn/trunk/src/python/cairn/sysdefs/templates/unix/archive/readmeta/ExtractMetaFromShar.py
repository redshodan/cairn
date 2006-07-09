"""templates.unix.archive.readmeta.ExtractMetaFromShar Module"""


import os
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
		metaFile = cairn.mktemp("cairn-metafile-")
		cairn.verbose("Extracting metafile to: " + metaFile[1])
		sysdef.info.setChild("archive/metafilename", metaFile[1])
		try:
			xml = archive.read(pos)
			os.write(metaFile[0], xml)
			os.close(metaFile[0])
			archive.close()
		except Exception, err:
			raise cairn.Exception("Unable to write meta file %s: %s" % \
								  (metaFile[1], err))
		return


	def run(self, sysdef):
		archive = self.openFile(sysdef)
		pos = self.findMetaEnd(sysdef, archive)
		self.writeMeta(sysdef, archive, pos)
		return True
