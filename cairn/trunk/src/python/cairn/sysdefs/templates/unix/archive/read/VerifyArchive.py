"""templates.unix.read.VerifyArchive Module"""



import os
import os.path
import tempfile

import cairn
from cairn import Options
from cairn.sysdefs import SystemInfo



def getClass():
	return VerifyArchive()



class VerifyArchive(object):

	def compareShar(self, sysdef):
		if (sysdef.info.get("archive/shar-offset") !=
			sysdef.readInfo.get("archive/shar-offset")):
			raise cairn.Exception("Corrupt archive file %s: shar offset is incorrect" % sysdef.info.get("archive/filename"))
		return


	def compareSize(self, sysdef):
		fileName = sysdef.info.get("archive/filename")
		size = 0
		try:
			info = os.stat(fileName)
			size = "%d" % info[stat.ST_SIZE]
		except Exception, err:
			raise cairn.Exception("Failed to stat archive file %s: %s" % \
								  (fileName, err))
		if size != long(sysdef.info.get("archive/size")):
			raise cairn.Exception("Corrupt archive file %s: incorrect size" % sysdef.info.get("archive/filename"))
		return


	def openFile(self, sysdef):
		filename = sysdef.info.get("archive/filename")
		try:
			archive = file(filename, "rb")
			archive.seek(int(sysdef.info.get("archive/shar-offset")))
		except Exception, err:
			raise cairn.Exception("Unable to open archive file %s: %s" % \
								  (filename, err))
		return archive


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
		return sum.hexdigest()


	def compareMD5s(self, sysdef, theMD5sum):
		if theMD5sum != sysdef.readInfo.get("archive/md5sum"):
			raise cairn.Exception("Corrupt archive file %s: incorrect md5sum" % sysdef.info.get("archive/filename"))
		return


	def run(self, sysdef):
		if sysdef.info.get("archive/shar"):
			self.compareShar(sysdef)
		self.compareSize(sysdef)
		archive = self.openfile(sysdef)
		theMD5sum = self.md5sum(archive)
		archive.close()
		self.compareMD5s(sydef, theMD5sum)
		return true
