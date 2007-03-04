"""cairn.cmds.meta"""



from cairn import Options
from cairn.cmds.Command import Command
from cairn.cmds.meta.Edit import Edit
from cairn.cmds.meta.Extract import Extract
from cairn.cmds.meta.Replace import Replace
from cairn.cmds.meta.Unshar import Unshar



class Meta(Command):

	def __init__(self, libname, fullCmdLine):
		super(Meta, self).__init__(libname, fullCmdLine)
		self._subCmds = {"edit":Edit(libname, fullCmdLine, self),
						 "extract":Extract(libname, fullCmdLine, self),
						 "replace":Replace(libname, fullCmdLine, self),
						 "unshar":Unshar(libname, fullCmdLine, self)}
		return


	def name(self):
		return "meta"


	def getHelpDesc(self):
		return "Extract or edit the metadata of this image file"


	def getHelpShortDesc(self):
		return "Extract or edit the metadata of this image file"


	def getHelpUsage(self):
		return "cairn meta <subcmd> [options] <image file>"


	def getSubCmds(self):
		return self._subCmds



def getClass():
	return Meta
