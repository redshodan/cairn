"""templates.unix.copy.RunArchiver Module"""


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
	return RunArchiver()



class Percent(object):
	def __init__(self, estimated):
		self.estimated = estimated
		self.read = 0l
		self.lastPercent = 0



class RunArchiver(object):
	IN = 1
	OUT = 2


	def prepare(self, sysdef):
		raise cairn.Exception("Unimplemented function")
		return


	def direction(self):
		raise cairn.Exception("Unimplemented function")
		return


	def runTools(self, sysdef, archive):
		input = None
		output = None
		if self.direction() == self.IN:
			input = archive
		else:
			output = archive
		archiveTool = Process.startCmd("archive/archive-tool",
									   sysdef.info.get("archive/archive-tool-cmd"),
									   None, None, None)
		zipTool = Process.startCmd("archive/zip-tool",
								   sysdef.info.get("archive/zip-tool-cmd"),
								   input, output, None)
		self.runPipe(sysdef, archiveTool, zipTool)
		try:
			archive.close()
		except:
			pass
		return


	def runPipe(self, sysdef, archiveTool, zipTool):
		percent = Percent(long(sysdef.info.get("archive/estimated-size")))
		if self.direction() == self.IN:
			input = zipTool
			output = archiveTool
			readfds = [input.stdout, archiveTool.stderr, zipTool.stderr,
					   output.stdout]
		else:
			input = archiveTool
			output = zipTool
			readfds = [input.stdout, archiveTool.stderr, zipTool.stderr]
		running = True
		self.displayPercent(0)
		errStr = ""
		while (running and (len(readfds) > 0)):
			(selrfds, trash1, trash2) = select.select(readfds, [], [], 0)
			for sel in selrfds:
				if sel == input.stdout:   ### Archive output
					try:
						buff = os.read(input.stdout, 524288)   ### 512K
					except Exception, err:
						errStr = str(err)
						try: os.close(readfds[0])
						except: pass
						del readfds[0]
					if not buff:
						running = False
						break
					try:
						os.write(output.stdin, buff)
					except Exception, err:
						errStr = str(err)
						try: os.close(readfds[0])
						except: pass
						del readfds[0]
					self.processPercent(percent, len(buff))
				# Monitor stdout on the archive when its the output, for extract
				if ((output == archiveTool) and (sel == output.stdout)):
					try:
						buff = os.read(output.stdout, 512)
					except Exception, err:
						errStr = str(err)
						try: os.close(readfds[0])
						except: pass
						del readfds[0]
					if buff and len(buff):
						cairn.displayRaw(buff)
				if ((sel == archiveTool.stderr) and not archiveTool.readErr()):
					readfds.remove(archiveTool.stderr)
				if ((sel == zipTool.stderr) and	not zipTool.readErr()):
					readfds.remove(zipTool.stderr)
		self.finishDisplayPercent()
		input.wait()
		output.wait()
		cairn.debug("Archive tool exit: %d stderr:\n%s" % (archiveTool.exit(),
														   archiveTool.err))
		cairn.debug("Zip tool exit: %d stderr:\n%s" % (zipTool.exit(), zipTool.err))
		err = "Error running archiver: %s\n" % errStr
		if archiveTool.err:
			err = "\nError running archive tool: %s" % archiveTool.err
		if zipTool.err:
			err = err + "\nError running zip tool: %s" % zipTool.err
		if not self.verifyExit(archiveTool, zipTool):
			raise cairn.Exception("Error running a tool: archiver exited with %d, zipper exited with %d: %s" % (archiveTool.exit(), zipTool.exit(), err))
		return


	def processPercent(self, percent, buffSize):
		percent.read = percent.read + buffSize
		cur = int((float(percent.read) / float(percent.estimated)) *
				  100)
		if cur != percent.lastPercent:
			percent.lastPercent = cur
			self.displayPercent(cur)
		return


	def displayPercent(self, percent):
		cairn.displayRaw("\r%d%%  " % percent)
		sys.stdout.flush()
		return


	def finishDisplayPercent(self):
		self.displayPercent(100)
		cairn.displayNL()
		return


	def verifyExit(self, archiveTool, zipTool):
		if (archiveTool.exit() != 0) or (zipTool.exit() != 0):
			return False
		else:
			return True


	def run(self, sysdef):
		try:
			archive = self.prepare(sysdef)
			self.runTools(sysdef, archive)
		except Exception, err:
			raise cairn.Exception("Failed while running archive tools: %s" % err)
		return True
