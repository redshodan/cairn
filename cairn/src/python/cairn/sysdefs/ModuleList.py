"""Module lists"""


import string

import cairn
from cairn import sysdefs


class ModuleList(object):
	__moduleList = None


	def __init__(self):
		return


	def load(self, sysDef, sysInfo):
		modules = sysDef.getModuleList()
		moduleNames = []
		for module in string.split(modules, ";"):
			module = string.replace(module, " ", "")
			if len(module) > 0:
				moduleNames.append(module)
		self.__moduleList = sysdefs.loadModules(sysDef.className(),
												sysDef.classTemplate(), moduleNames)
		return


	def run(self, sysDef, sysInfo):
		for module in self.__moduleList:
			if cairn.verbose():
				print "Running module: " + module.__name__
			func = getattr(module, "run")
			if not func(sysDef, sysInfo):
				raise cairn.Exception("Failed to run module: " + module.__name__)
		return
