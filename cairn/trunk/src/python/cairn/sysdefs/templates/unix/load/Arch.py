"""Generic unix.load.Arch Module"""


import os
import re

import cairn



def getClass():
	return Arch()



class Arch(object):
	def run(self, sysdef):
		sysname, nodename, release, version, machine = os.uname()
		sysdef.info.set("arch/cpu", machine)
		if re.compile("i[3456]86").match(machine):
			sysdef.info.set("arch/name", "i386")
		elif ((machine == "ia64") or (machine == "x86_64") or
			  (machine == "ppc")):
			sysdef.info.set("arch/name", machine)
		return True
