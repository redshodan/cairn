"""linux.unknown.archive.read.RunArchiver Module"""




import cairn
from cairn.sysdefs.linux import Shared
import cairn.sysdefs.templates.unix.archive.read.RunArchiver as tmpl


def getClass():
	return RunArchiver()



class RunArchiver(tmpl.RunArchiver):

	def verifyExit(self, archiveTool, zipTool):
		return Shared.verifyToolsExit(archiveTool, zipTool)
