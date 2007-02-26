"""templates.unix.system.Paths Module"""


import cairn
from cairn.sysdefs import Tools
from cairn import Options



def getClass():
	return Paths()



class Paths(object):

	def __init__(self):
		self.__PATH = ""
		self.__BINS = []
		return


	def userCheck(self, sysdef):
		return


	def getPath(self, sysdef):
		if Options.get("path"):
			return Options.get("path")
		elif sysdef.info.get("env/path"):
			return sysdef.info.get("env/path")
		return self.__PATH


	def getBins(self, sysdef):
		return self.__BINS


	def run(self, sysdef):
		Tools.findTools(sysdef, self.getPath(sysdef), self.getBins(sysdef))
		self.userCheck(sysdef)
		return True
