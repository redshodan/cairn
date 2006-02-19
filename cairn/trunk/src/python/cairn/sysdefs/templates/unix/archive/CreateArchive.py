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



class Percent(object):
	def __init__(self, size):
		self.size = size
		self.readTotal = 0
		self.readSize = 0
		self.readMeg = 0
		self.last = 0



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
		percent = None
		if sysdef.info.get("archive/adjusted-size"):
			percent = Percent(int(sysdef.info.get("archive/adjusted-size")))
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
					self.processPercent(percent, len(buff))
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
		self.finishDisplayPercent()
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


	def processPercent(self, percent, buffSize):
		if not percent:
			return
		percent.readTotal = percent.readTotal + buffSize
		percent.readMeg = percent.readMeg + buffSize
		if percent.readMeg > 1048576:
			percent.readMeg = percent.readMeg - 1048576
			percent.readSize = percent.readSize + 1
			if percent.readSize:
				cur = int((float(percent.readSize) / float(percent.size)) *
							  100)
			if cur != percent.last:
				print "total read/size=cur", percent.readTotal, \
					  percent.readSize, percent.size, cur
				percent.lastPercent = cur
				self.displayPercent(cur)
		return


	def displayPercent(self, percent):
		print "\r%d%%  " % percent,
		sys.stdout.flush()
		return


	def finishDisplayPercent(self):
		print
		return


	def run(self, sysdef):
		cairn.log("Creating archive")
		if sysdef.info.get("archive/shar"):
			archive = self.prepShar(sysdef)
		else:
			archive = self.prepArchive(sysdef)
		self.runTools(sysdef, archive)
		return True
