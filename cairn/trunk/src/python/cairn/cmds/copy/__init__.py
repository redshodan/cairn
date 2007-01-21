"""cairn.cmds.copy"""



from cairn import Options
from cairn.cmds.Command import Command



class Copy(Command):

	def getModuleString(self):
		return "system.CheckRoot; system; copy; ui.Shutdown"


	def name(self):
		return "copy"


	def getOptMaps(self):
		return (Options.cliCopyRestoreCommonOpts, Options.cliCopyOpts)


	def getHelpDesc(self):
		return "Create a CAIRN image of this machine. The image file name is optional. If not specified it will be automatically generated using the machines hostname and todays date. See the description of '--help' for more advanced help options."


	def getHelpShortDesc(self):
		return "Create an image of this computer"


	def getHelpUsage(self):
		return "%prog copy [options] [image file]"



def getClass():
	return Copy
