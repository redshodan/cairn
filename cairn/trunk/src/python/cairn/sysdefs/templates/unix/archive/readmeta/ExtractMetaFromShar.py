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


	def readMeta(self, sysdef, archive):
		meta = ""
		while True:
			buff = archive.read(512)
			if not buff:
				break
			meta = meta + buff
			pos = meta.find("__ARCHIVE__")
			if pos >= 0:
				return meta[:pos]
		raise cairn.Exception("Invalid image file.")
		return


	def writeMeta(self, sysdef, archive, meta):
		# 12 = len("__ARCHIVE__\n")
		sysdef.info.setChild("archive/shar-offset", "%d" % (len(meta) + 12))
		metaFile = cairn.mktemp("cairn-metafile-")
		cairn.verbose("Extracting metafile to: " + metaFile[1])
		sysdef.info.setChild("archive/metafilename", metaFile[1])
		try:
			os.write(metaFile[0], meta)
			os.close(metaFile[0])
			archive.close()
		except Exception, err:
			raise cairn.Exception("Unable to write meta file %s: %s" % \
								  (metaFile[1], err))
		return


	def run(self, sysdef):
		archive = self.openFile(sysdef)
		meta = self.readMeta(sysdef, archive)
		self.writeMeta(sysdef, archive, meta)
		return True
