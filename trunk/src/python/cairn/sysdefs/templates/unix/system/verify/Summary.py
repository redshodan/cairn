"""templates.unix.system.Summary Module"""


import cairn
from cairn import Options



def getClass():
	return Summary()



class Summary(object):

	def run(self, sysdef):
		cairn.log("System has been verified as being supported")
		return True
