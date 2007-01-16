""" cairn.sysdefs.darwin.unknown.__init__
	Unknown Darwin system definitions"""


import cairn
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
		cairn.log("System definition:  %s Darwin" % (self.name()))
		return
