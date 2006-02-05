"""templates.unix.copy.EstimateSize Module"""


import os

import cairn
from cairn import Options



def getClass():
	return EstimateSize()



class EstimateSize(object):

	def run(self, sysdef):
		if sysdef.info.get("archive/excludes"):
			return True
		return True


