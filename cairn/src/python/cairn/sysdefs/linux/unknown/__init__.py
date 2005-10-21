"""Unknown Linux system definitions"""


import sys
import os
import re

import cairn
import cairn.Options as Options
from cairn import sysdefs
from cairn.sysdefs.SystemInfo import *



def getPlatform():
	return Unknown()



class Unknown:
	def __init__(self):
		return


	def matchPartial(self):
		return False


	def matchExact(self):
		return False


	def name(self):
		return "Unknown"


	def className(self):
		return "cairn.sysdefs.linux.unknown"


	def load(self):
		return


	def getModuleList(self):
		if Options.get("program") == "copy":
			return self.getCopyModuleList()
		else:
			return self.getRestoreModuleList()
		return
	

	def getCopyModuleList(self):
		return "LoadOS; LoadArch; copy.LoadPaths;"


	def getRestoreModuleList(self):
		return "LoadOS; LoadArch; restore.LoadPaths;"


	def printSummary(self):
		print "System definition:  %s Linux" % (self.name())
		return
