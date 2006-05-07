"""templates.unix.archive.read.Tools Module"""



def getClass():
	return Tools()



#
# Current approach is have the archive command pass the archive to stdout,
# catch that with ccopy so it can get a percent done based on byte throughput,
# then pass along to a zip command which outputs to stdout, which is redirected
# to disk.
#


class Tools(object):

	def setArchiveCmd(self, sysdef):
		return False


	def setZipCmd(self, sysdef):
		return False


	def run(self, sysdef):
		if not self.setArchiveCmd(sysdef):
			return False
		if not self.setZipCmd(sysdef):
			return False
		return True
