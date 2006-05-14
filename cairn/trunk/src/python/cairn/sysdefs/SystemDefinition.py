"""cairn.sysdefs.SystemDefinition - System definition base class"""


import cairn



from cairn.sysdefs import SystemInfo
from cairn import Options
from cairn import sysdefs
from cairn.sysdefs import IModule



class SystemDefinition(object):
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


	def getModuleString(self):
		return self.getInitModuleString() + self.programModuleStr


	def setModuleString(self, programModuleStr):
		self.programModuleStr = programModuleStr
		return


	def getInitModuleString(self):
		return "system;"


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
