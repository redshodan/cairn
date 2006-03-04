"""cairn.sysdefs.SystemDefinition - System definition base class"""


import cairn



from cairn.sysdefs import SystemInfo
from cairn import Options
from cairn import sysdefs
from cairn.sysdefs import IModule



class SystemDefinition(object):
	def __init__(self):
		self.info = SystemInfo.createNew()
		self.moduleList = None
		return


	def matchPartial(self):
		return False


	def matchExact(self):
		return False


	def load(self):
		return


	def getModuleString(self):
		if Options.get("program") == "copy":
			return self.getInitModuleString() + self.getCopyModuleString()
		elif Options.get("program") == "restore":
			return self.getInitModuleString() + self.getRestoreModuleString()
		return


	def getInitModuleString(self):
		return "system;"


	def getCopyModuleString(self):
		return "archive;"


	def getRestoreModuleString(self):
		return ""


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
