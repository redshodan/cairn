"""cairn.copy.copy"""



from cairn import Program



class Copy(Program.Program):

	def getModuleString(self):
		return "ui; system; copy; ui.Shutdown"


	def name(self):
		return "copy"



def run(libname):
	Program.run(Copy, libname)
	return
