"""cairn.cmds.extract"""



from cairn import Options
from cairn.cmds.Command import Command



class Extract(Command):

	def getModuleString(self):
		return "system.OS; system.Arch; system.Machine; system.Paths; extract;"


	def name(self):
		return "extract"


	def allowBadOpts(self):
		return True


	def getOptMaps(self):
		return (Options.cliExtractOpts,)


	def getHelpDesc(self):
		return "Extract portions of this image file. See the description of '--help' for more advanced help options. This is a frontend to the image tool used to create the image. Any of the options after the -- will be passed on to the image tool. By default this is 'tar'. This can run the image tool without having to extract the image from the CAIRN image file while still exposing virtually all of that image tools funtionality."


	def getHelpShortDesc(self):
		return "Extract files or edit metadata in this image file"


	def getHelpUsage(self):
		return "%prog extract [options] <image file> [-- [image tool options]]"



def getClass():
	return Extract
