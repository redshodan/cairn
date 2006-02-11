"""templates.unix.copy.CreateArchive Module"""


#
# This will need to be refactored I'm sure. Just get something done right now.
#


import os
import popen2
import select
import shutil

import cairn
from cairn import Options



def getClass():
	return CreateArchive()



class CreateArchive(object):

	def prepArchive(self, sysdef):
		fileName = sysdef.info.get("archive/filename")
		try:
			return os.open(fileName, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % (fileName,
																		  err))
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
			raise cairn.Exception("Failed to open archive file %s: %s" % (fileName,
																		  err))


	def runTools(self, sysdef, archive):
		archiveTool = self.startTool(sysdef, "archive/archive-tool-cmd", None, None,
											None)
		zipTool = self.startTool(sysdef, "archive/zip-tool-cmd", None, archive, None)
		self.runPipe(sysdef, archiveTool, zipTool)
		return


	def startArchiveTool(self, sysdef):
		cmd = sysdef.info.get("archive/archive-tool-cmd")
		cairn.verbose("Running: %s" % (cmd))
		try:
			os.chdir("/")
			pipes = popen2.popen3(cmd.split())
		except Exception, err:
			raise cairn.Exception("Failed to run command '%s': %s" % (cmd, err))
		return [pipes[0], pipes[2]]


	def startTool(self, sysdef, tool, stdin, stdout, stderr):
		cmd = sysdef.info.get(tool)
		cairn.verbose("Running: %s" % (cmd))
		if not stdin:
			pstdin = os.pipe()
		if not stdout:
			pstdout = os.pipe()
		if not stderr:
			pstderr = os.pipe()
		pid = os.fork()
		if pid == 0:
			if stdin:
				os.dup2(stdin, 0)
			else:
				os.dup2(pstdin[0], 0)
				os.close(pstdin[0])
				os.close(pstdin[1])
			if stdout:
				os.dup2(stdout, 1)
			else:
				os.dup2(pstdout[1], 1)
				os.close(pstdout[0])
				os.close(pstdout[1])
			if stderr:
				os.dup2(stderr, 2)
			else:
				os.dup2(pstderr[1], 2)
				os.close(pstderr[0])
				os.close(pstderr[1])
			arr = cmd.split()
			os.execv(arr[0], arr)
			raise cairn.Exception("Failed to exec command: %s" % (cmd))
		else:
			ret = []
			if stdin:
				ret.append(stdin)
			else:
				ret.append(pstdin[1])
				os.close(pstdin[0])
			if stdout:
				ret.append(stdout)
			else:
				ret.append(pstdout[0])
				os.close(pstdout[1])
			if stderr:
				ret.append(stderr)
			else:
				ret.append(pstderr[0])
				os.close(pstderr[1])
			return ret
		return


	def runPipe(self, sysdef, archiveTool, zipTool):
		size = 0
		if sysdef.info.get("archive/adjusted-size"):
			size = int(sysdef.info.get("archive/adjusted-size"))
		readSize = 0
		lastPercent = 0
		archiveErr = ""
		zipErr = ""
		readfds = [archiveTool[2], zipTool[2], archiveTool[1]]
		running = True
		while running:
			(selrfds, trash1, trash2) = select.select(readfds, [], [], 0)
			for sel in selrfds:
				if sel == archiveTool[1]:   ### Archive output
					buff = os.read(archiveTool[1], int(1024))  ### 1M
					if not buff:
						running = False
						break
					os.write(zipTool[0], buff)
				if sel == archiveTool[2]:   ### Archive err
					buff = os.read(archiveTool[2], int(1024))  ### 1M
					print "read archive error:", len(buff), buff
					archiveErr = archiveErr + buff
				if sel == zipTool[2]:   ### Zip err
					buff = os.read(zipTool[2], int(1024))  ### 1M
					print "read zip error:", len(buff), buff
					archiveErr = zipErr + buff
		os.close(archiveTool[0])
		os.close(archiveTool[1])
		os.close(archiveTool[2])
		os.close(zipTool[0])
		os.close(zipTool[1])
		os.close(zipTool[2])
		if archiveErr:
			cairn.error("Error running archive tool: %s" % archiveErr)
		if zipErr:
			cairn.error("Error running zip tool: %s" % zipErr)
		if archiveErr or zipErr:
			raise cairn.Exception("Error running a tool")
		return


	def run(self, sysdef):
		if sysdef.info.get("archive/shar"):
			archive = self.prepShar(sysdef)
		else:
			archive = self.prepArchive(sysdef)
		self.runTools(sysdef, archive)
		return True
