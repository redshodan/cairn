"""templates.unix.system.Paths Module"""


import cairn
import cairn.sysdefs as sysdefs
from cairn import Options
from cairn.sysdefs import Tools



def getClass():
	return Paths()



class Paths(object):

	def __init__(self):
		self.__PATH = ""
		self.__BINS = []

	def getPath(self, sysdef):
		if sysdef.info.get("env/path"):
			return sysdef.info.get("env/path")
		return self.__PATH


	def getBins(self, sysdef):
		return self.__BINS


	def run(self, sysdef):
		Tools.findTools(sysdef, self.getPath(sysdef), self.getBins(sysdef))
		return True
