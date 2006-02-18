""" cairn.sysdefs.linux.unknown.__init__
	Unknown Linux system definitions"""


import cairn.sysdefs.templates.unix as tmpl



def getClass():
	return Unknown()



class Unknown(tmpl.UNIX):
	def __init__(self):
		super(Unknown, self).__init__()
		return


	def name(self):
		return "Unknown"


	def __printSummary(self):
		print "System definition:  %s Linux" % (self.name())
		return
