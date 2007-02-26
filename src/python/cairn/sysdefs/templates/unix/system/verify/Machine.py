"""templates.unix.system.verify.Machine Module"""



import cairn



def getClass():
	return Machine()



class Machine(object):

	def run(self, sysdef):
		if not sysdef.info.get("machine/name"):
			cairn.warn("Could not figure out hostname")
		return True
