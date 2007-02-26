"""cairn.cmds.meta.Edit"""



from cairn import Options
from cairn.cmds.Command import Command



class Edit(Command):

	def __init__(self, libname, fullCmdLine, parent):
		super(Edit, self).__init__(libname, fullCmdLine)
		self._parent = parent
		return


	def parent(self):
		return self._parent


	def getModuleString(self):
		return "system.OS; system.Arch; system.Machine; system.Paths; archive.readmeta; meta.edit;"


	def name(self):
		return "edit"


	def getHelpDesc(self):
		return "Edit the metadata of this image file"


	def getHelpShortDesc(self):
		return "Edit the metadata of this image file"


	def getHelpUsage(self):
		return "%prog meta edit [options] <image file>"


	def getOptMaps(self):
		return (Options.cliMetaEditOpts,)



def getClass():
	return Edit
