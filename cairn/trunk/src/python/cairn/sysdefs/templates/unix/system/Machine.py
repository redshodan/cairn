"""templates.unix.system.Machine Module"""


import platform

import cairn



def getClass():
	return Machine()



class Machine(object):

	def run(self, sysdef):
		if platform.node() and len(platform.node()):
			sysdef.info.setChild("machine/name", platform.node())
		return True
