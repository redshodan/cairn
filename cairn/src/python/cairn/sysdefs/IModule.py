"""Pseudo Inheritable Modules"""


import os
import sys
import re
import string

import cairn
from cairn import Options


def loadList(sysDef):
	modules = sysDef.getModuleList()
	moduleNames = []
	for module in string.split(modules, ";"):
		module = string.replace(module, " ", "")
		if len(module) > 0:
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
	# Find corresponding modules following the module 'hierarchy'. For each try
	# the program version then the main module.
	modules = []
	for name in moduleNames:
		found = False
		for curRoot in sysDef.__class__.__mro__:
			fullName = "%s.%s.%s" % (curRoot.__module__, Options.get("program"), name)
			cairn.verbose("Looking for %s" % fullName)
			if loadAModule(fullName, modules):
				found = True
				cairn.verbose("Found %s" % fullName)
				break
			fullName = "%s.%s" % (curRoot.__module__, name)
			cairn.verbose("Looking for %s" % fullName)
			if loadAModule(fullName, modules):
				found = True
				cairn.verbose("Found %s" % fullName)
				break
		if not found:
			raise cairn.Exception(cairn.ERR_MODULE,
								  "Unable to import module %s" % (name))
	return modules


def loadModulesByName(root, moduleNames):
	modules = []
	for name in moduleNames:
		if loadAModule("%s.%s" % (root, name), modules):
			continue
		raise cairn.Exception(cairn.ERR_MODULE,
							  "Unable to import module %s" % (name))
	return modules


def loadAModule(module, modules):
	try:
		__import__(module)
		modules.append(sys.modules[module])
		return True
	except ImportError, err:
		return False
