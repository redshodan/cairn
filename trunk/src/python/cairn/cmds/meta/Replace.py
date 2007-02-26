"""cairn.cmds.meta.Replace"""



from cairn import Options
from cairn.cmds.Command import Command



class Replace(Command):

	def __init__(self, libname, fullCmdLine, parent):
		super(Replace, self).__init__(libname, fullCmdLine)
		self._parent = parent
		return


	def parent(self):
		return self._parent


	def getModuleString(self):
		return "system.OS; system.Arch; system.Machine; system.Paths; archive.readmeta; meta.Replace; archive.mergemeta;"


	def name(self):
		return "replace"


	def getHelpDesc(self):
		return "Replace the metadata of this image file"


	def getHelpShortDesc(self):
		return "Replace the metadata of this image file"


	def getHelpUsage(self):
		return "cairn meta replace [options] <image file> [meta file]"


	def allowBadOpts(self):
		return True



def getClass():
	return Replace
