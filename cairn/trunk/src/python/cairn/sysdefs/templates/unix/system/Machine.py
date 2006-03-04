"""templates.unix.load.Machine Module"""


import platform

import cairn



def getClass():
	return Machine()



class Machine(object):

	def run(self, sysdef):
		if not platform.node() or (len(platform.node()) <= 0):
			cairn.warn("Could not figure out hostname")
		else:
			sysdef.info.setChild("machine/name", platform.node())
		return True
