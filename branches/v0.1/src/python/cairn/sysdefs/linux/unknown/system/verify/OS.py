"""templates.unix.system.verify.OS Module"""



import os



def getClass():
	return OS()



class OS(object):

	def run(self, sysdef):
		if sysdef.info.get("os/version-short") != "2.6":
			raise cairn.Exception("Invalid kernel version %s detected. Currently only the 2.6 kernel is supported." % sysdef.info.get("os/version-short"))
		return True
