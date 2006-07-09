"""cairn.extract - Extraction frontend for image files"""



from cairn import Program



class Extract(Program.Program):

	def getModuleString(self):
		return "system; extract;"


	def name(self):
		return "extract"



def run():
	Program.run(Extract)
	return
