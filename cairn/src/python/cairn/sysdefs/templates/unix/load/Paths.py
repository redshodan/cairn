"""Generic unix.load.Paths system definitions"""


import cairn
import cairn.sysdefs as sysdefs



def getClass():
	return Paths()



class Paths(object):
	def __init__(self):
		self.__PATH = ""
		self.__BINS = {"ERROR" : "Invalid base function called"}

	def getPath(self):
		return self.__PATH


	def getBins(self):
		return self.__BINS


	def run(self, sysdef, sysinfo):
		sysdefs.findPaths(self.getPath(), self.getBins())
		return True
