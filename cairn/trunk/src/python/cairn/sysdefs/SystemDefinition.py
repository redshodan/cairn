"""cairn.sysdefs.SystemDefinition - System definition base class"""


import cairn



from cairn.sysdefs import SystemInfo
from cairn import Options
from cairn import sysdefs
from cairn.sysdefs import IModule



class SystemDefinition(object):

	# Base types
	UNIX = 0
	WINDOWS = 1

	def __init__(self):
		self.info = SystemInfo.createNew()
		self.readInfo = None
		self.moduleList = None
		self.programModuleStr = None
		return


	def matchPartial(self):
		return False


	def matchExact(self):
		return False


	def load(self):
		return


	def quit(self):
		sysdefs.quit()
		return


	def __printSummary(self):
		return


	def printSummary(self):
		self.__printSummary()
		self.info.printSummary()
		return


	def printMeta(self):
		self.info.printXML()
		return


	def init(self):
		return True


	def getBaseType(self):
		raise cairn.Exception("Unimplemented function")
