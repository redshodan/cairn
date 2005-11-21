"""Unknown Linux LoadOS Module"""


import cairn.sysdefs.templates.unix.LoadOS as tmpl



def getClass():
	return LoadOS()



class LoadOS(tmpl.LoadOS):
	def __init__(self):
		return


	def nameOS(self):
		return "Linux"
