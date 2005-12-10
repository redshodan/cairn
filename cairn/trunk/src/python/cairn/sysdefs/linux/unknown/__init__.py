""" cairn.sysdefs.linux.unknown.__init__
	Unknown Linux system definitions"""


from cairn.sysdefs.templates.unix import *



def getClass():
	return Unknown()



class Unknown(UNIX):
	def __init__(self):
		return


	def name(self):
		return "Unknown"


	def printSummary(self):
		print "System definition:  %s Linux" % (self.name())
		return
