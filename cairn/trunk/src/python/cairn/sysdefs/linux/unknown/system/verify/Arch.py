"""templates.unix.system.verify.Arch Module"""



import cairn



def getClass():
	return Arch()



class Arch(object):

	def run(self, sysdef):
		if sysdef.info.get("arch/name") != "i386":
			raise cairn.exception("Invalid architecture %s detected. Currently only i386 is correctly supported." % sysdef.info.get("arch/name"))
		return True
