"""cairn.sysdefs.templates.unix.__init__
   Generic UNIX definitions"""


import sys
import os
import re

import cairn
import cairn.Options as Options
from cairn import sysdefs
from cairn.sysdefs.SystemInfo import *



def getPlatform():
	return Unknown()



class UNIX:
	def __init__(self):
		return


	def matchPartial(self):
		return False


	def matchExact(self):
		return False


	def name(self):
		return "UNIX"


	def className(self):
		return "cairn.sysdefs.templates.unix"


	def load(self):
		return


	def getModuleList(self):
		return self.getInitModuleList() + self.getMainModuleList()


	def getInitModuleList(self):
		return "LoadOS; LoadArch; LoadPaths;"

	def getMainModuleList(self):
		return ""


	def printSummary(self):
		print "System definition:  Generic UNIX"
		return
