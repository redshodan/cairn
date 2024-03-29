"""darwin.unknown.archive.write.RunArchiver Module"""



import cairn
from cairn.sysdefs.utils import GNUTools
import cairn.sysdefs.templates.unix.archive.write.RunArchiver as tmpl



def getClass():
	return RunArchiver()



class RunArchiver(tmpl.RunArchiver):

	def verifyExit(self, archiveTool, zipTool):
		return GNUTools.verifyToolsExit(archiveTool, zipTool)
