""" cairn.sysdefs.linux.unknown.__init__
	Unknown Linux system definitions"""


from cairn.sysdefs.templates.unix import *



def getPlatform():
	return Unknown()



class Unknown(UNIX):
	def __init__(self):
		return


	def name(self):
		return "Unknown"


	def className(self):
		return "cairn.sysdefs.linux.unknown"


	def printSummary(self):
		print "System definition:  %s Linux" % (self.name())
		return
