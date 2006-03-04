"""linux.unknown.system.Arch Module"""


import re
import string

import cairn.sysdefs.templates.unix.system.Arch as tmpl



def getClass():
	return Arch()



class Arch(tmpl.Arch):
	def __init__(self):
		return


	def run(self, sysdef):
		if not super(Arch, self).run(sysdef):
			return false

		modelNameRE = re.compile("^model name")
		cpuinfo = file("/proc/cpuinfo", "r")
		for line in cpuinfo.readlines():
			if modelNameRE.match(line):
				line = string.strip(line)
				arr = line.split(": ")
				sysdef.info.setChild("arch/cpu-str", arr[1])
		cpuinfo.close()
		return True
