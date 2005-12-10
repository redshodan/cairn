""" cairn.sysdefs.linux.unknown.__init__
	Unknown Linux system definitions"""


from cairn.sysdefs.templates.unix import *



def getClass():
	return Unknown()



class Unknown(UNIX):
	def __init__(self):
		super(Unknown, self).__init___()
		return


	def name(self):
		return "Unknown"


	def __printSummary(self):
		print "System definition:  %s Linux" % (self.name())
		return
