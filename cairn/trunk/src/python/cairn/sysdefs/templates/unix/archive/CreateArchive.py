"""templates.unix.copy.CreateArchive Module"""


#
# This will need to be refactored I'm sure. Just get something done right now.
#


import os
import select
import shutil
import sys

import cairn
from cairn import Options
from cairn.sysdefs.templates.unix.misc import Process



def getClass():
	return CreateArchive()



class CreateArchive(object):

	def prepArchive(self, sysdef):
		fileName = sysdef.info.get("archive/filename")
		try:
			return os.open(fileName, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % \
								  (fileName, err))
		return


	def prepShar(self, sysdef):
		metaFileName = sysdef.info.get("archive/metafilename")
		fileName = sysdef.info.get("archive/filename")
		try:
			shutil.copyfile(metaFileName, fileName)
			archive = os.open(fileName, os.O_WRONLY | os.O_APPEND)
			os.write(archive, "\n__ARCHIVE__\n")
			os.fsync(archive)
			return archive
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % \
								  (fileName, err))


	def runTools(self, sysdef, archive):
		archiveTool = Process.startCmd("archive/archive-tool",
									   sysdef.info.get("archive/archive-tool-cmd"),
									   None, None, None)
		zipTool = Process.startCmd("archive/zip-tool-cmd",
								   sysdef.info.get("archive/zip-tool-cmd"),
								   None, archive, None)
		self.runPipe(sysdef, archiveTool, zipTool)
		try:
			archive.close()
		except:
			pass
		return


	def runPipe(self, sysdef, archiveTool, zipTool):
		size = 0
		if sysdef.info.get("archive/adjusted-size"):
			size = int(sysdef.info.get("archive/adjusted-size"))
		readTotal = 0
		readSize = 0
		readMeg = 0
		lastPercent = 0
		readfds = [ archiveTool.stdout, archiveTool.stderr, zipTool.stderr]
		running = True
		self.displayPercent(0)
		while running:
			(selrfds, trash1, trash2) = select.select(readfds, [], [], 0)
			for sel in selrfds:
				if sel == archiveTool.stdout:   ### Archive output
					buff = os.read(archiveTool.stdout, 524288)   ### 512K
					if not buff:
						running = False
						break
					os.write(zipTool.stdin, buff)
					if size:
						readTotal = readTotal + len(buff)
						readMeg = readMeg + len(buff)
						if readMeg > 1048576:
							readMeg = readMeg - 1048576
							readSize = readSize + 1
							if readSize:
								percent = int((float(readSize) / float(size)) *
											  100)
							if percent != lastPercent:
								#print "total read/size=per", readTotal, \
								#	  readSize, size, percent
								lastPercent = percent
								self.displayPercent(percent)
				if sel == archiveTool.stderr:   ### Archive err
					buff = os.read(archiveTool.stderr, 1024)
					if buff:
						archiveTool.err = archiveTool.err + buff
					else:
						readfds.remove(archiveTool.stderr)
				if sel == zipTool.stderr:   ### Zip err
					buff = os.read(zipTool.stderr, 1024)
					if buff:
						zipTool.err = zipTool.err + buff
					else:
						readfds.remove(zipTool.stderr)
		print
		archiveTool.wait()
		zipTool.wait()
		err = ""
		if archiveTool.err:
			err = "Error running archive tool: %s" % archiveTool.err
		if zipTool.err:
			err = err + "Error running zip tool: %s" % zipTool.err
		if (archiveTool.exit() != 0) or (zipTool.exit() != 0):
			raise cairn.Exception("Error running a tool: %s" % err)
		return


	def displayPercent(self, percent):
		print "\r%d%%  " % percent,
		sys.stdout.flush()
		return


	def run(self, sysdef):
		cairn.log("Creating archive")
		if sysdef.info.get("archive/shar"):
			archive = self.prepShar(sysdef)
		else:
			archive = self.prepArchive(sysdef)
		self.runTools(sysdef, archive)
		return True
