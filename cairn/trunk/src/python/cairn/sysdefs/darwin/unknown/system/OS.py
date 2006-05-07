"""darwin.unknown.system.OS Module"""


import cairn.sysdefs.templates.unix.system.OS as tmpl



def getClass():
	return OS()



class OS(tmpl.OS):
	def nameOS(self):
		return "Darwin"
