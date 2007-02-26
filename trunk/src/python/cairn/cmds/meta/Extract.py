"""cairn.cmds.meta.Extract"""



from cairn import Options
from cairn.cmds.Command import Command



class Extract(Command):

	def __init__(self, libname, fullCmdLine, parent):
		super(Extract, self).__init__(libname, fullCmdLine)
		self._parent = parent
		return


	def parent(self):
		return self._parent


	def getModuleString(self):
		return "system.OS; system.Arch; system.Machine; system.Paths; archive.readmeta; meta.Save;"


	def name(self):
		return "extract"


	def getHelpDesc(self):
		return "Extract the metadata of this image file"


	def getHelpShortDesc(self):
		return "Extract the metadata of this image file"


	def getHelpUsage(self):
		return "cairn meta extract [options] <image file> [meta file]"


	def allowBadOpts(self):
		return True



def getClass():
	return Extract
