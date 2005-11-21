""" cairn.sysdefs.darwin.unknown.__init__
	Unknown Darwin system definitions"""


from cairn.sysdefs.templates.unix import *



def getClass():
	return Unknown()



class Unknown(UNIX):
	def __init__(self):
		return


	def name(self):
		return "Unknown"


	def className(self):
		return "cairn.sysdefs.darwin.unknown"


	def classTemplate(self):
		return "cairn.sysdefs.templates.unix"


	def printSummary(self):
		print "System definition:  %s Darwin" % (self.name())
		return
