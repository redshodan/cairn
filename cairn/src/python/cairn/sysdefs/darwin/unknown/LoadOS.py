"""Unknown Darwin LoadOS Module"""


import cairn.sysdefs.templates.unix.LoadOS as tmpl



class LoadOS(tmpl.LoadOS):
	def __init__(self):
		return


	def nameOS(self):
		return "Darwin"


def run(sysdef, sysinfo):
	mod = LoadOS()
	return mod.run(sysdef, sysinfo)
