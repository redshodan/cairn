"""Unknown Linux LoadArch Module"""


import re

import cairn.sysdefs.templates.unix.LoadArch as tmpl



class LoadArch(tmpl.LoadOS):
	def __init__(self):
		return


	def run(self, sysdef, sysinfo):
		if not super(LoadArch).run():
			return false

		modelNameRE = re.compile("^model name")
		cpuinfo = file("/proc/cpuinfo", "r")
		for line in cpuinfo.readlines():
			if modelNameRE.match(line):
				arr = line.split(": ")
				sysinfo.set("CPU_STR", arr[1])
		cpuinfo.close()
		return True


def run(sysdef, sysinfo):
	mod = LoadArch()
	return mod.run(sysdef, sysinfo)
