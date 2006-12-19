"""cairn.verify.verify - Verify frontend for image files"""



from cairn import Program



class Verify(Program.Program):

	def getModuleString(self):
		return "system.OS; system.Arch; system.Machine; system.Paths; verify;"


	def name(self):
		return "verify"


	def disableLogging(self):
		return True


def run(libname):
	Program.run(Verify, libname)
	return
