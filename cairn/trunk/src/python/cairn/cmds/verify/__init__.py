"""cairn.cmds.verify"""



from cairn import Options
from cairn.cmds.Command import Command



class Verify(Command):

	def getModuleString(self):
		return "system.OS; system.Arch; system.Machine; system.Paths; verify;"


	def name(self):
		return "verify"


	def disableLogging(self):
		return True


	def getOptMaps(self):
		return (Options.cliVerifyOpts,)


	def getHelpDesc(self):
		return "Verify the integrity of this image file."


	def getHelpUsage(self):
		return "%prog verify [options] <image file>"



def getClass():
	return Verify
