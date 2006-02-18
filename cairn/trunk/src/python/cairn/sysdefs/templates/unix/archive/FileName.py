"""templates.unix.archive.FileName Module"""



import cairn
import time


def getClass():
	return FileName()



class FileName(object):

	def genFileName(self, sysdef):
		hostname = sysdef.info.get("machine/name")
		if not hostname:
			hostname = "cairn-image"
		date = time.strftime("%Y-%m-%d.cimg")
		return "%s-%s" % (hostname, date)


	def run(self, sysdef):
		if not sysdef.info.get("archive/filename"):
			sysdef.info.set("archive/filename", self.genFileName(sysdef))
		return True
