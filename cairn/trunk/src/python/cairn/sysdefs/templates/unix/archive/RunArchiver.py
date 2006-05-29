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
		zipTool = Process.startCmd("archive/zip-tool-cmd",
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
			input = zipTool.stdout
			output = archiveTool.stdin
		else:
			input = archiveTool.stdout
			output = zipTool.stdin
		readfds = [ input, archiveTool.stderr, zipTool.stderr]
		running = True
		self.displayPercent(0)
		while running:
			(selrfds, trash1, trash2) = select.select(readfds, [], [], 0)
			for sel in selrfds:
				if sel == input:   ### Archive output
					buff = os.read(input, 524288)   ### 512K
					if not buff:
						running = False
						break
					os.write(output, buff)
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
		percent.read = percent.read + buffSize
		cur = int((float(percent.read) / float(percent.estimated)) *
				  100)
		if cur != percent.lastPercent:
			percent.lastPercent = cur
			self.displayPercent(cur)
		return


	def displayPercent(self, percent):
		print "\r%d%%  " % percent,
		sys.stdout.flush()
		return


	def finishDisplayPercent(self):
		self.displayPercent(100)
		print
		return


	def run(self, sysdef):
		archive = self.prepare(sysdef)
		self.runTools(sysdef, archive)
		return True
