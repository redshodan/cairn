"""cairn.cmds.meta.Unshar"""



from cairn import Options
from cairn.cmds.Command import Command



class Unshar(Command):

	def __init__(self, libname, fullCmdLine, parent):
		super(Unshar, self).__init__(libname, fullCmdLine)
		self._parent = parent
		return


	def parent(self):
		return self._parent


	def getModuleString(self):
		return "system.OS; system.Arch; system.Machine; system.Paths; archive.readmeta; meta.unshar;"


	def name(self):
		return "unshar"


	def getHelpDesc(self):
		return "Unshar the image. Removes the metadata placing it in FILE and leaves the bare underlying archive in the image file."


	def getHelpShortDesc(self):
		return "Unshar the metadata of this image file"


	def getHelpUsage(self):
		return "cairn meta unshar [options] <image file> [meta file]"


	def allowBadOpts(self):
		return True



def getClass():
	return Unshar
