"""CAIRN Restore Class"""



from cairn import Program
from cairn import sysdefs



class Restore(Program.Program):

	def setDefaults(self):
		self._defaults["env/mountdir"] = "/mnt/cairn-restore"
		return


	def getModuleString(self):
		return "system; restore;"


	def name(self):
		return "restore"



def run(libname):
	Program.run(Restore, libname)
	return
