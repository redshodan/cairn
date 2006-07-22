"""cairn.extract - Extraction frontend for image files"""



from cairn import Program



class Extract(Program.Program):

	def getModuleString(self):
		return "system.OS; system.Arch; system.Machine; system.Paths; extract;"


	def name(self):
		return "extract"


	def allowBadOpts(self):
		return True


def run(libname):
	Program.run(Extract, libname)
	return
