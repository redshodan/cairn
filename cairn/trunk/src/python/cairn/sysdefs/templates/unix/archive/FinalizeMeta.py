"""templates.unix.copy.FinalizeMeta Module"""


import os
import os.path

import cairn
from cairn import Options



def getClass():
	return FinalizeMeta()



class FinalizeMeta(object):

	def run(self, sysdef):
		if not sysdef.info.get("archive/shar"):
			return True
		return True
