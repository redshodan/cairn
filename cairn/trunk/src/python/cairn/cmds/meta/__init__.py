"""cairn.cmds.meta"""



from cairn import Options
from cairn.cmds.Command import Command



class Meta(Command):

	def getModuleString(self):
		return "system.OS; system.Arch; system.Machine; system.Paths; extract;"


	def name(self):
		return "meta"


	def allowBadOpts(self):
		return True


	def getOptMaps(self):
		return (Options.cliExtractOpts,)


	def getHelpDesc(self):
		return "Extract or edit the metadata of this image file"


	def getHelpShortDesc(self):
		return "Extract or edit the metadata of this image file"


	def getHelpUsage(self):
		return "%prog extract [options] <image file> [-- [image tool options]]"



def getClass():
	return Meta
