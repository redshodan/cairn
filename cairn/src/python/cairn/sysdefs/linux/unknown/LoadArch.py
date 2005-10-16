"""Unknown Linux LoadArch Module"""


import os
import re

import cairn





def run(sysdef, sysinfo):
	sysname, nodename, release, version, machine = os.uname()
	sysinfo.set("CPU", machine)
	if re.compile("i[3456]86").match(machine):
		sysinfo.set("ARCH", "i386")
	elif ((machine == "ia64") or (machine == "x86_64") or
		  (machine == "ppc")):
		sysinfo.set("ARCH", machine)

	modelNameRE = re.compile("^model name")
	cpuinfo = file("/proc/cpuinfo", "r")
	for line in cpuinfo.readlines():
		if modelNameRE.match(line):
			arr = line.split(": ")
			sysinfo.set("CPU_STR", arr[1])
	cpuinfo.close()
	return True
