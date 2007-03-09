"""darwin.unknown.archive.read.RunArchiver Module"""



import cairn
from cairn.sysdefs.util import GNUTools
import cairn.sysdefs.templates.unix.archive.read.RunArchiver as tmpl



def getClass():
	return RunArchiver()



class RunArchiver(tmpl.RunArchiver):

	def verifyExit(self, archiveTool, zipTool):
		return GNUTools.verifyToolsExit(archiveTool, zipTool)
