"""cairn.copy.copy"""



from cairn import Program



class Copy(Program.Program):

	def getModuleString(self):
		return "system; copy;"


	def name(self):
		return "copy"



def run(libname):
	Program.run(Copy, libname)
	return
