"""templates.unix.verify.Summary Module"""



import cairn
from cairn import Options



def getClass():
	return Summary()


class Summary(object):


	def run(self, sysdef):
		cairn.display("Archive verified")
		return True
