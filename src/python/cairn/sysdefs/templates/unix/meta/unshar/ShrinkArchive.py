"""templates.unix.archive.meta.unshar.ShrinkMeta Module"""


import os

import cairn.sysdefs.templates.unix.archive.mergemeta.WriteMeta as tmpl
import cairn



def getClass():
	return ShrinkArchive()



class ShrinkArchive(tmpl.WriteMeta):

	def includeMeta(self):
		return False


	def userMsg(self):
		cairn.info("Removing metadata from image, this can take a long time")
		return


	def writeFile(self, sysdef, archive):
		try:
			offset = sysdef.info.getInt("archive/original-shar-offset")
			length = 0
			if offset != length:
				# Make room for the newer larger meta
				bs = 4096
				delta = length - offset
				archive.seek(0, 2)
				orgLen = archive.tell()
				total = orgLen - offset
				count = total / bs
				remainder = total % bs
				for index in xrange(count):
					pos = offset + index * bs
					archive.seek(pos, 0)
					buff = archive.read(bs)
					archive.seek(pos + delta, 0)
					archive.write(buff)
				archive.seek(offset + total * bs, 0)
				buff = archive.read(remainder)
				archive.seek(offset + (total - 1) * bs, 0)
				archive.write(buff)
				# Prepare to truncate if need be
				archive.flush()
				os.fsync(archive.fileno())
				if delta < 0:
					os.ftruncate(archive.fileno(), orgLen + delta)
				archive.seek(0, 0)
			if self.includeMeta():
				archive.write(meta)
				archive.write("\n__ARCHIVE__\n")
			archive.close()
		except Exception, err:
			raise cairn.Exception("Failed to write metadata file", err)
		return
