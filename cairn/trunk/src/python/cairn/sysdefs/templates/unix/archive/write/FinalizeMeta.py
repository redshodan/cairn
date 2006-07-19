"""templates.unix.archive.write.FinalizeMeta Module"""


import os
import stat
import md5

import cairn
from cairn import Options
from cairn.sysdefs import SystemInfo



def getClass():
	return FinalizeMeta()



class FinalizeMeta(object):

	def sizeArchive(self, fileName):
		try:
			info = os.stat(fileName)
			return "%d" % info[stat.ST_SIZE]
		except Exception, err:
			raise cairn.Exception("Failed to stat archive file %s: %s" % \
								  (fileName, err))
		return


	def openArchive(self, fileName):
		try:
			return file(fileName, "r+")
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % \
								  (fileName, err))
		return


	def readMeta(self, archive):
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


	def findOffset(self, archive, meta):
		# 12 = len("__ARCHIVE__\n")
		pos = len(meta) + 12
		archive.seek(pos)
		return "%d" % pos


	def md5sum(self, sysdef, archive):
		cairn.log("MD5 summing archive file")
		sum = md5.new()
		running = True
		while running:
			buff = archive.read(4096)
			if buff and len(buff) > 0:
				sum.update(buff)
			else:
				running = False
				break
		return sum.hexdigest()


	def writeHeaders(self, archive, meta, sum, size, offset):
		self.findPositions(meta, sum, size, offset)
		self.writeValue(archive, sum)
		self.writeValue(archive, size)
		self.writeValue(archive, offset)
		return


	def findPositions(self, meta, sum, size, offset):
		archivePos = meta.find("<archive>")
		sum[3] = meta.find(sum[0], archivePos) + len(sum[0])
		size[3] = meta.find(size[0], archivePos) + len(size[0])
		offset[3] = meta.find(offset[0], archivePos) + len(offset[0])
		return


	def writeValue(self, archive, value):
		if len(value[1]) != value[2]:
			buff = "".zfill(value[2] - len(value[1]))
			value[1] = buff + value[1]
		archive.seek(value[3])
		archive.write(value[1])
		return


	def run(self, sysdef):
		if not sysdef.info.get("archive/shar"):
			return True
		cairn.log("Finalizing archive file")
		fileName = sysdef.info.get("archive/filename")
		size = self.sizeArchive(fileName)
		archive = self.openArchive(fileName)
		meta = self.readMeta(archive)
		offset = self.findOffset(archive, meta)
		sum = self.md5sum(sysdef, archive)
		self.writeHeaders(archive, meta,
						  ["<md5sum>", sum, SystemInfo.PADDING_MD5, 0],
						  ["<size>", size, SystemInfo.PADDING_INT, 0],
						  ["<shar-offset>", offset, SystemInfo.PADDING_INT, 0])
		archive.close()
		return True
