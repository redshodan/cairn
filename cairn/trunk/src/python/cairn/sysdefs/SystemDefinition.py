"""cairn.sysdefs.SystemDefinition - System definition base class"""


import cairn



from cairn.sysdefs.SystemInfo import *
from cairn.sysdefs import IModule



class SystemDefinition(object):
	def __init__(self):
		self.info = SystemInfo()
		self.moduleList = None
		return


	def matchPartial(self):
		return False


	def matchExact(self):
		return False


	def load(self):
		return


	def getModuleString(self):
		return ""


	def __printSummary(self):
		return


	def printSummary(self):
		self.__printSummary()
		self.info.printSummary()
		return
