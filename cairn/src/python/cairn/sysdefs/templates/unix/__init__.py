"""cairn.sysdefs.templates.unix.__init__
   Generic UNIX definitions"""


import sys
import os
import re

import cairn
import cairn.Options as Options
from cairn import sysdefs
from cairn.sysdefs.SystemInfo import *



def getClass():
	return UNIX()



class UNIX(object):
	def __init__(self):
		return


	def matchPartial(self):
		return False


	def matchExact(self):
		return False


	def name(self):
		return "UNIX"


	def load(self):
		return


	def getModuleList(self):
		return "load;"


	def getInitModuleList(self):
		return "load.OS; load.Arch; load.Paths;"

	def getMainModuleList(self):
		return ""


	def printSummary(self):
		print "System definition:  Generic UNIX"
		return
