"""linux.unknown.system.OS Module"""


import cairn.sysdefs.templates.unix.system.OS as tmpl



def getClass():
	return OS()



class OS(tmpl.OS):
	def __init__(self):
		return


	def nameOS(self):
		return "Linux"
