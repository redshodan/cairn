"""darwin.unknown.load.OS Module"""


import cairn.sysdefs.templates.unix.load.OS as tmpl



def getClass():
	return OS()



class OS(tmpl.OS):
	def nameOS(self):
		return "Darwin"
