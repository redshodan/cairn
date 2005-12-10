""" cairn.sysdefs.darwin.unknown.__init__
	Unknown Darwin system definitions"""


from cairn.sysdefs.templates.unix import *



def getClass():
	return Unknown()



class Unknown(UNIX):
	def __init__(self):
		super(Unknown, self).__init__()
		return


	def name(self):
		return "Unknown"


	def __printSummary(self):
		print "System definition:  %s Darwin" % (self.name())
		return