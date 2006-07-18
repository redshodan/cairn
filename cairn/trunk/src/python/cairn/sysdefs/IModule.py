"""Pseudo Inheritable Modules"""


import os
import sys

import cairn
from cairn import Options
from cairn.sysdefs import ModuleSpec
from cairn.sysdefs import UserModule
from cairn.sysdefs import UserShellModule


def loadList(sysdef, moduleSpec, userModuleSpec, moduleList, prefix):
	modInfos = ModuleSpec.parseModuleSpec(sysdef, moduleSpec, userModuleSpec,
										  prefix)
	str = ""
	for mod in modInfos:
		str = "%s; %s" % (str, mod.getValue())
	cairn.debug("Module list: %s" % str.lstrip(";").strip())
	loadModulesByInst(sysdef, modInfos, userModuleSpec, moduleList)
	return


def loadModulesByInst(sysdef, moduleInfos, userModuleSpec, moduleList):
	"""Find corresponding modules following the module 'hierarchy'. For each try
	   the program version then the main module."""
	for modInfo in moduleInfos:
		if modInfo.type == ModuleSpec.USER_MOD_SHELL:
			createUserShellModule(sysdef, modInfo.getValue(), moduleList)
		elif modInfo.type == ModuleSpec.USER_MOD_PY:
			createUserModule(sysdef, modInfo.getValue(), moduleList)
		else:
			names = modInfo.getNames()
			workingInfos = []
			for name in names:
				info = ModuleSpec.ModuleInfo()
				info.copy(modInfo)
				info.name = name
				workingInfos.append(info)
			for info in workingInfos:
				for curRoot in sysdef.__class__.__mro__:
					foundModule = loadAModule("%s.%s.%s" %
											  (curRoot.__module__,
											   Options.get("program"),
											   info.name))
					if foundModule:
						break
					foundModule = loadAModule("%s.%s" % (curRoot.__module__,
														 info.name))
					if foundModule:
						break
				if not foundModule:
					raise cairn.Exception("Unable to import module %s" %
										  name)
				info.module = foundModule
				if not checkSubModule(sysdef, info, userModuleSpec, moduleList):
					moduleList.append(info)
	return


def checkSubModule(sysdef, info, userModuleSpec, moduleList):
	getSubModuleString = None
	try:
		getSubModuleString = getattr(info.module, "getSubModuleString")
	except AttributeError:
		return False
	moduleNames = getSubModuleString(sysdef)
	if not moduleNames:
		return True
	try:
		getClass = getattr(info.module, "getClass")
		moduleList.append(info)
	except AttributeError:
		pass
	subModules = ModuleList(sysdef)
	cairn.debug("Found sub-module %s: %s" % (info.name, moduleNames))
	loadList(sysdef, moduleNames, userModuleSpec, subModules, info.name)
	for subModule in subModules.iter():
		moduleList.append(subModule)
	return True


def loadModulesByName(root, moduleNames, modules):
	for name in moduleNames:
		module = loadAModule("%s.%s" % (root, name))
		if not module:
			raise cairn.Exception("Unable to import module %s" % name)
		modules.append(module)
	return


def loadAModule(module):
	cairn.debug("  Looking for %s" % module)
	try:
		__import__(module)
		try:
			getattr(sys.modules[module], "empty")
			return None
		except:
			cairn.debug("Found %s" % module)
			return sys.modules[module]
	except ImportError, err:
		return None


def findFileInPath(path, file, seperator = ":"):
	paths = path.split(seperator)
	for part in paths:
		fullname = part + "/" + file
		try:
			os.stat(fullname)
			return fullname
		except:
			pass
	return None


def createUserShellModule(sysdef, str, modules):
	mod = sys.modules["cairn.sysdefs.UserShellModule"]
	modules.append(ModuleSpec.ModuleInfo(module=mod, args={"code":str},
										 type=ModuleSpec.USER_MOD_SHELL))
	return


def createUserModule(sysdef, str, modules):
	mod = sys.modules["cairn.sysdefs.UserModule"]
	modules.append(ModuleSpec.ModuleInfo(module=mod, args={"code":str},
										 type=ModuleSpec.USER_MOD_PY))
	return



class ModuleList(object):
	"""cairn.sysdefs.IModule.ModuleList - A list of modules to run"""


	def __init__(self, sysdef):
		self.__list = []
		self.__curModule = 0
		self.__sysdef = sysdef


	def iter(self):
		return self.__list


	def next(self):
		self.__curModule = self.__curModule + 1
		return


	def append(self, module):
		self.__list.append(module)
		return


	def me(self):
		return self.__curModule


	def name(self, index):
		return getattr(self.__list[index].module, "__name__")


	def find(self, name):
		index = 0
		for modInfo in self.__list:
			if getattr(modInfo.module, "__name__") == name:
				return index
			index = index + 1
		return -1


	def replace(self, name, newModName):
		index = self.find(name)
		if index < 0:
			raise cairn.Exception("Unable to import module %s" % newModName)
		module = loadAModule(newModName)
		if not module:
			raise cairn.Exception("Unable to import module %s" % newModName)
		self.__list[index].module = module
		return True


	def insertAfterMe(self, newModName):
		moduleList = ModuleList(self.__sysdef)
		loadList(self.__sysdef, newModName, None, moduleList, None)
		modInfos = moduleList.iter()
		if len(modInfos) <= 0:
			raise cairn.Exception("Unable to import module %s" % newModName)
		modInfos.reverse()
		for modInfo in modInfos:
			self.__list.insert(self.__curModule + 1, modInfo)
		return True


	def toStrings(self):
		strs = []
		for modInfo in self.__list:
			strs.append("%s" % modInfo.module.__name__)
		return strs
