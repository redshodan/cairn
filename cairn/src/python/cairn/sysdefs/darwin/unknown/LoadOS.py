"""Unknown Darwin LoadOS Module"""


import cairn.sysdefs.templates.unix.LoadOS as tmpl



def getClass():
	return LoadOS()



class LoadOS(tmpl.LoadOS):
	def nameOS(self):
		return "Darwin"
