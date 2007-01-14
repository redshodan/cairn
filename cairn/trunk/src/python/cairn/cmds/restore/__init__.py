"""cairn.cmds.restore"""



from cairn import Options
from cairn.cmds.Command import Command



class Restore(Command):

	def setDefaults(self):
		self._defaults["env/mountdir"] = "/mnt/cairn-restore"
		return


	def getModuleString(self):
		return "system; restore;"


	def name(self):
		return "restore"


	def getOptMaps(self):
		return (Options.cliCopyRestoreCommonOpts, Options.cliRestoreOpts)


	def getHelpDesc(self):
		return "Restore a CAIRN image onto this machine. See the description of '--help' for more advanced help options."


	def getHelpShortDesc(self):
		return "Restore an image to this computer"


	def getHelpUsage(self):
		return "%prog restore [options] <image file>"



def getClass():
	return Restore
