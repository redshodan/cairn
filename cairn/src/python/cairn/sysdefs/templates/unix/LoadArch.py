"""Generic UNIX LoadArch Module"""


import os
import re

import cairn



def getClass():
	return LoadArch()



class LoadArch(object):
	def run(self, sysdef, sysinfo):
		sysname, nodename, release, version, machine = os.uname()
		sysinfo.set("CPU", machine)
		if re.compile("i[3456]86").match(machine):
			sysinfo.set("ARCH", "i386")
		elif ((machine == "ia64") or (machine == "x86_64") or
			  (machine == "ppc")):
			sysinfo.set("ARCH", machine)
		return True
