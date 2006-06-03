"""Pseudo Inheritable Modules"""


import os
import sys

import cairn
from cairn import Options
from cairn.sysdefs import ModuleSpec


def loadList(sysdef, moduleSpec, userModuleSpec, modules, prefix):
	moduleNames = ModuleSpec.parseModuleSpec(sysdef, moduleSpec, userModuleSpec, prefix)
	cairn.debug("Module list:", moduleNames)
	loadModulesByInst(sysdef, moduleNames, userModuleSpec, modules)
	return


def loadModulesByInst(sysdef, moduleNames, userModuleSpec, modules):
	"""Find corresponding modules following the module 'hierarchy'. For each try
	   the program version then the main module."""
	for name in moduleNames:
		foundModule = None
		for curRoot in sysdef.__class__.__mro__:
			foundModule = loadAModule("%s.%s.%s" % (curRoot.__module__,
													Options.get("program"), name))
			if foundModule:
				break
			foundModule = loadAModule("%s.%s" % (curRoot.__module__, name))
			if foundModule:
				break
		if not foundModule:
			raise cairn.Exception("Unable to import module %s" % (name),
								  cairn.ERR_MODULE)
		if not checkSubModule(sysdef, name, foundModule, userModuleSpec, modules):
			modules.append(foundModule)
	return


def checkSubModule(sysdef, name, module, userModuleSpec, modules):
	getSubModuleString = None
	try:
		getSubModuleString = getattr(module, "getSubModuleString")
	except AttributeError:
		return False
	try:
		getClass = getattr(module, "getClass")
		modules.append(module)
	except AttributeError:
		pass
	moduleNames = getSubModuleString(sysdef)
	subModules = ModuleList(sysdef)
	cairn.debug("Found sub-module %s: %s" % (name, moduleNames))
	loadList(sysdef, moduleNames, userModuleSpec, subModules, name)
	for subModule in subModules.iter():
		modules.append(subModule)
	return True


def loadModulesByName(root, moduleNames, modules):
	for name in moduleNames:
		module = loadAModule("%s.%s" % (root, name))
		if not module:
			raise cairn.Exception("Unable to import module %s" % (name),
								  cairn.ERR_MODULE)
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
		return getattr(self.__list[index], "__name__")


	def find(self, name):
		index = 0
		for module in self.__list:
			if getattr(module, "__name__") == name:
				return index
			index = index + 1
		return -1


	def replace(self, name, newModName):
		index = self.find(name)
		if index < 0:
			raise cairn.Exception("Unable to import module %s" % (newModName),
								  cairn.ERR_MODULE)
		module = loadAModule(newModName)
		if not module:
			raise cairn.Exception("Unable to import module %s" % (newModName),
								  cairn.ERR_MODULE)
		self.__list[index] = module
		return True


	def insertAfterMe(self, newModName):
		moduleList = ModuleList(self.__sysdef)
		loadList(self.__sysdef, newModName, None, moduleList, None)
		modules = moduleList.iter()
		if len(modules) <= 0:
			raise cairn.Exception("Unable to import module %s" % (newModName),
								  cairn.ERR_MODULE)
		modules.reverse()
		for module in modules:
			self.__list.insert(self.__curModule + 1, module)
		return True


	def toString(self, padding = ", ", eol = ""):
		str = ""
		for module in self.__list:
			str = "%s%s%s%s" % (str, padding, module.__name__, eol)
		return str
