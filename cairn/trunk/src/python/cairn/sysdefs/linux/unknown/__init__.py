""" cairn.sysdefs.linux.unknown.__init__
	Unknown Linux system definitions"""


import cairn
from cairn import cloader
from cairn import sysdefs
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
		cairn.log("System definition:  %s Linux" % (self.name()))
		return


	def setup(self):
		prog = sysdefs.getProgram()
		cloader.load(sysdefs.getDef(), prog.getLibname(), "thirdparty",
					 "pylibparted")
		return True
