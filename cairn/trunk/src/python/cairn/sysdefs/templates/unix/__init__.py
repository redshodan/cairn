"""cairn.sysdefs.templates.unix.__init__
   Generic UNIX definitions"""


import cairn
from cairn.sysdefs.SystemDefinition import *



def getClass():
	return UNIX()



class UNIX(SystemDefinition):
	def __init__(self):
		super(UNIX, self).__init__()
		return


	def name(self):
		return "UNIX"


	def __printSummary(self):
		cairn.log("System definition:  Generic UNIX")
		return
