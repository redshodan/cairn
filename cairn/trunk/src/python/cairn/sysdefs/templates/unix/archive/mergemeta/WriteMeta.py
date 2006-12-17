"""templates.unix.archive.mergemeta.WriteMeta Module"""


import os
import os.path

import cairn
from cairn import Options



def getClass():
	return WriteMeta()



class WriteMeta(object):

	def openArchive(self, sysdef):
		filename = sysdef.info.get("archive/filename")
		try:
			archive = file(filename, "r+")
			return archive
		except Exception, err:
			raise cairn.Exception("Failed to open archive file", err)
		return


	def writeFile(self, sysdef, archive):
		try:
			meta = sysdef.readInfo.toStr()
			# 13 = len("\n__ARCHIVE__\n")
			offset = sysdef.info.getInt("archive/original-shar-offset")
			length = len(meta) + 13
			if offset < length:
				# Make room for the newer larger meta
				bs = 4096
				delta = length - offset
				archive.seek(0, 2)
				orgLen = archive.tell()
				total = orgLen - offset
				count = total / bs
				remainder = total % bs
				for index in xrange(count):
					pos = offset + total - (index + 1) * bs
					archive.seek(pos, 0)
					buff = archive.read(bs)
					archive.seek(pos + delta, 0)
					archive.write(buff)
				archive.seek(offset, 0)
				buff = archive.read(remainder)
				archive.seek(length, 0)
				archive.write(buff)
				archive.seek(0, 0)
			archive.write(meta)
			archive.write("\n__ARCHIVE__\n")
			archive.close()
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file", err)
		return


	def run(self, sysdef):
		cairn.info("Writing new meta file to image")
		archive = self.openArchive(sysdef)
		self.writeFile(sysdef, archive)
		return True
