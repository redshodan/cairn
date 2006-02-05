"""templates.unix.copy.CreateArchive Module"""


#
# This will need to be refactored I'm sure. Just get something done right now.
#


import os
import shutil

import cairn
from cairn import Options



def getClass():
	return CreateArchive()



class CreateArchive(object):

	def prepArchive(self, sysdef):
		fileName = sysdef.info.get("archive/filename")
		try:
			return file(fileName, "w")
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % (fileName,
																		  err))
		return


	def prepShar(self, sysdef):
		metaFileName = sysdef.info.get("archive/metafilename")
		fileName = sysdef.info.get("archive/filename")
		try:
			shutil.copyfile(metaFileName, fileName)
			archive = file(fileName, "a")
			archive.write("\n__ARCHIVE__\n")
			return archive
		except Exception, err:
			raise cairn.Exception("Failed to open archive file %s: %s" % (fileName,
																		  err))


	def runTools(self, sysdef, archive):
		archiveTool = self.startTool(sysdef, archive, "archive/archive-cmd-line")
		zipTool = self.startTool(sysdef, archive, "archive/zip-cmd-line")
		self.runPipe(sysdef, archiveTool, zipTool)
		return


	def startTool(sysdef, archive, tool):
		cmd = sysdef.info.get(tool)
		try:
			pipes = os.popen3(cmd, "b")
		except Exception, err:
			raise cairn.Exception("Failed to run command '%s': %s" % (cmd, err))
		return pipes


	def runPipe(sysdef, archiveTool, zipTool):
		return


	def run(self, sysdef):
		if sysdef.info.get("archive/shar"):
			archive = self.prepShar(sysdef)
		else:
			archive = self.prepArchive(sysdef)
		self.runArchiveTools(sysdef, archive)
		return True


