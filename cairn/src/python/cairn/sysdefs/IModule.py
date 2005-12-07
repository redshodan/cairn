"""Pseudo Inheritable Modules"""


import os
import sys
import re
import string

import cairn
from cairn import Options


def loadList(sysDef, moduleString, prefix = None):
	moduleNames = []
	for module in string.split(moduleString, ";"):
		module = string.replace(module, " ", "")
		if len(module) > 0:
			if prefix:
				moduleNames.append("%s.%s" % (prefix, module))
			else:
				moduleNames.append(module)
	return loadModulesByInst(sysDef, moduleNames)


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


def loadModulesByInst(sysDef, moduleNames):
	"""Find corresponding modules following the module 'hierarchy'. For each try
	   the program version then the main module."""
	modules = []
	for name in moduleNames:
		foundModule = None
		for curRoot in sysDef.__class__.__mro__:
			fullName = "%s.%s.%s" % (curRoot.__module__, Options.get("program"), name)
			cairn.verbose("Looking for %s" % fullName)
			foundModule = loadAModule(fullName)
			if foundModule:
				cairn.verbose("Found %s" % fullName)
				break
			fullName = "%s.%s" % (curRoot.__module__, name)
			cairn.verbose("Looking for %s" % fullName)
			foundModule = loadAModule(fullName)
			if foundModule:
				cairn.verbose("Found %s" % fullName)
				break
		if not foundModule:
			raise cairn.Exception(cairn.ERR_MODULE,
								  "Unable to import module %s" % (name))
		if not checkSubModule(sysDef, name, foundModule, modules):
			modules.append(foundModule)
	return modules


def checkSubModule(sysDef, name, module, modules):
	try:
		func = getattr(module, "getSubModules")
	except AttributeError:
		return False
	moduleNames = func()
	subModules = loadList(sysDef, moduleNames, name)
	for subModule in subModules:
		modules.append(subModule)
	return True


def loadModulesByName(root, moduleNames):
	modules = []
	for name in moduleNames:
		module = loadAModule("%s.%s" % (root, name))
		if not module:
			raise cairn.Exception(cairn.ERR_MODULE,
								  "Unable to import module %s" % (name))
		modules.append(module)
	return modules


def loadAModule(module):
	try:
		__import__(module)
		try:
			getattr(sys.modules[module], "empty")
			return None
		except:
			return sys.modules[module]
	except ImportError, err:
		return None
