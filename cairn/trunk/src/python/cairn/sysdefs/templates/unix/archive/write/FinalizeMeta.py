"""templates.unix.copy.write.FinalizeMeta Module"""


import os
import stat
import md5
import re

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
			return file(fileName, "r")
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % \
								  (fileName, err))
		return


	def findOffset(self, archive):
		pos = 0
		for line in archive:
			pos = pos + len(line)
			if line.startswith("__ARCHIVE__"):
				break
		archive.seek(pos)
		return "%d" % pos


	def md5sum(self, archive):
		sum = md5.new()
		running = True
		while running:
			buff = archive.read(4096)
			if buff and len(buff) > 0:
				sum.update(buff)
			else:
				running = False
				break
		archive.close()
		return sum.hexdigest()


	def writeHeaders(self, fileName, sum, size, offset):
		self.findPositions(fileName, sum, size, offset)
		archive = os.open(fileName, os.O_RDWR)
		self.writeValue(archive, sum)
		self.writeValue(archive, size)
		self.writeValue(archive, offset)
		os.close(archive)
		return


	def findPositions(self, fileName, sum, size, offset):
		archive = file(fileName, "r")
		md5Re = re.compile("<md5sum>")
		sizeRe = re.compile("<size>")
		offsetRe = re.compile("<shar-offset>")
		pos = 0
		found = 0
		for line in archive:
			pos = pos + len(line)
			if md5Re.search(line):
				sum[2] = pos
				found = found + 1
			elif sizeRe.search(line):
				size[2] = pos
				found = found + 1
			elif offsetRe.search(line):
				offset[2] = pos
				found = found + 1
			if found == 3:
				break
		archive.close()
		return


	def writeValue(self, archive, value):
		if len(value[0]) != value[1]:
			buff = "".zfill(value[1] - len(value[0]))
			value[0] = buff + value[0]
		os.lseek(archive, value[2], 0)
		running = True
		while running:
			c = os.read(archive, 1)
			if c == "0":
				os.lseek(archive, -1, 1)
				os.write(archive, value[0])
				break
		return


	def run(self, sysdef):
		if not sysdef.info.get("archive/shar"):
			return True
		cairn.log("MD5 summing archive file")
		fileName = sysdef.info.get("archive/filename")
		size = self.sizeArchive(fileName)
		archive = self.openArchive(fileName)
		offset = self.findOffset(archive)
		sum = self.md5sum(archive)
		self.writeHeaders(fileName, [sum, SystemInfo.PADDING_MD5, 0],
						  [size, SystemInfo.PADDING_INT, 0],
						  [offset, SystemInfo.PADDING_INT, 0])
		return True
