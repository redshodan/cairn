"""templates.unix.restore.DisplayDone Module"""



import cairn



def getClass():
	return DisplayDone()



class DisplayDone(object):

	def run(self, sysdef):
		cairn.info("Restore finished")
		return True
