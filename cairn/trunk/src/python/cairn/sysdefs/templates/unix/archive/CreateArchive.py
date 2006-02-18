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



class ProcessInfo(object):
	def __init__(self):
		self.name = None
		self.pid = None
		self.stdin = None
		self.stdout = None
		self.stderr = None
		self.err = ""
		self.exitCode = 0
		return


	def wait(self):
		cairn.verbose("Waiting on: %s" % (self.name))
		self.close()
		try:
			self.exitCode = os.waitpid(self.pid, 0)[1]
		except Exception, err:
			raise cairn.Exception("Failed to wait for process %s: %s" % (self.name, err))
		return


	def close(self):
		try:
			os.close(self.stdin)
		except:
			pass
		try:
			os.close(self.stdout)
		except:
			pass
		try:
			os.close(self.stderr)
		except:
			pass


	def exit(self):
		return os.WEXITSTATUS(self.exitCode)



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
			ret = ProcessInfo()
			ret.name = tool
			ret.pid = pid
			if stdin:
				ret.stdin = stdin
			else:
				ret.stdin = pstdin[1]
				os.close(pstdin[0])
			if stdout:
				ret.stdout = stdout
			else:
				ret.stdout = pstdout[0]
				os.close(pstdout[1])
			if stderr:
				ret.stderr = stderr
			else:
				ret.stderr = pstderr[0]
				os.close(pstderr[1])
			return ret
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
								percent = int((float(readSize) / float(size)) * 100)
							if percent != lastPercent:
								print "total read/size=per", readTotal, readSize, size, percent
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
		print "%d%%" % percent


	def run(self, sysdef):
		if sysdef.info.get("archive/shar"):
			archive = self.prepShar(sysdef)
		else:
			archive = self.prepArchive(sysdef)
		self.runTools(sysdef, archive)
		return True
