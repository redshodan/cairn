"""templates.unix.system.CheckRoot Module"""


import os

import cairn
from cairn import Options



def getClass():
	return CheckRoot()



class CheckRoot(object):

	def run(self, sysdef):
		if os.getuid() != 0:
			raise cairn.UserEx("CAIRN %s must be run as root." %
							   Options.get("command"))
		return True
