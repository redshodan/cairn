"""Unknown Linux LoadArch Module"""


import re

import cairn.sysdefs.templates.unix.LoadArch as tmpl



def getClass():
	return LoadArch()



class LoadArch(tmpl.LoadArch):
	def __init__(self):
		return


	def run(self, sysdef, sysinfo):
		if not super(LoadArch, self).run(sysdef, sysinfo):
			return false

		modelNameRE = re.compile("^model name")
		cpuinfo = file("/proc/cpuinfo", "r")
		for line in cpuinfo.readlines():
			if modelNameRE.match(line):
				arr = line.split(": ")
				sysinfo.set("arch/cpu-str", arr[1])
		cpuinfo.close()
		return True
