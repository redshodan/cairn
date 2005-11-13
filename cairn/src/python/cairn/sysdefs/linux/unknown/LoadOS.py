"""Unknown Linux LoadOS Module"""



class LoadOS(cairn.sysdefs.templates.unix.LoadOS):
	def __init__(self):
		return


	def nameOS(self):
		return "Linux"


def run(sysdef, sysinfo):
	mod = LoadOS()
	return mod.run(sysdef, sysinfo)
