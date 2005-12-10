"""cairn.sysdefs.templates.unix.__init__
   Generic UNIX definitions"""


import sys
import os
import re

import cairn
import cairn.Options as Options
from cairn import sysdefs
from cairn.sysdefs.SystemDefinition import *



def getClass():
	return UNIX()



class UNIX(SystemDefinition):
	def __init__(self):
		super(UNIX, self).__init__()
		return


	def name(self):
		return "UNIX"


	def getModuleString(self):
		return "load;"


	def __printSummary(self):
		print "System definition:  Generic UNIX"
		return
