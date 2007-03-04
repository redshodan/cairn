"""templates.unix.copy.DisplayDone Module"""



import cairn



def getClass():
	return DisplayDone()



class DisplayDone(object):

	def run(self, sysdef):
		cairn.info("Archive finished")
		return True
