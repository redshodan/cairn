#
# CAIRN System definitions
#


import os
import sys
import re

import cairn
from cairn.sysdefs.SystemInfo import *


__sysDef = object()
__sysInfo = SystemInfo()
__sysModuleList = object()


def getDef():
	return __sysDef


def getInfo():
	return __info


def load():
	loadPlatform()
	loadModuleList()
	return


def loadPlatform():
	"""Platform selector"""

	import cairn.sysdefs.linux
	if linux.matchPlatform():
		cairn.sysdefs.__sysDef = linux.loadPlatform()
	else:
		raise cairn.Exception(cairn.ERR_SYSDEF, "Unable to determine the system definition for this machine.")
	return


def loadModuleList():
	from cairn.sysdefs.ModuleList import ModuleList
	cairn.sysdefs.__sysModuleList = ModuleList()
	cairn.sysdefs.__sysModuleList.load(cairn.sysdefs.__sysDef,
									   cairn.sysdefs.__sysInfo)
	return


def run():
	cairn.sysdefs.__sysModuleList.run(cairn.sysdefs.__sysDef,
									  cairn.sysdefs.__sysInfo)
	return


def printSummary():
	cairn.sysdefs.__sysDef.printSummary();
	cairn.sysdefs.__sysInfo.printSummary();
	return


###
### Utility functions used by sysdef modules.
###

def selectPlatform(root, moduleNames):
	defs = loadModules(root, moduleNames)

	partialMatches = []
	exactMatches = []
	for module in defs:
		platform = module.getPlatform()
		verifySysDef(partialMatches, exactMatches, platform)

	# Fall back to "Unknown" if none found
	if len(exactMatches) == 0:
		modules = loadModules(root, ["unknown"])
		if len(modules) == 1:
			platform = modules[0].getPlatform()
			verifySysDef([], [], platform)
			return platform
		else:
			raise cairn.Exception(cairn.ERR_SYSDEF, "No system definitions match this platform.")
	# Found one, run with it
	if len(exactMatches) == 1:
		return exactMatches[0]
	# Multiple modules think they are right
	elif len(exactMatches) > 1:
		print "There are mutiple system definition matchs:"
		for module in exactMatches:
			print "  ", module.__name__
		raise cairn.Exception(cairn.ERR_SYSDEF, "Multiple system definitions found. Please choose the correct one.")
	return


def verifySysDef(partialMatches, exactMatches, module):
	# Verify contents
	try:
		if (not (getattr(module, "matchPartial") and
				 getattr(module, "matchExact") and
				 getattr(module, "load") and
				 getattr(module, "printSummary"))
			and not cairn.Options.get("continue")):
			raise
	except:
		raise cairn.Exception(cairn.ERR_SYSDEF,
							  "Incomplete system definition code in module " +
							  str(module))
	func = getattr(module, "matchPartial")
	if func():
		partialMatches.append(module)
	func = getattr(module, "matchExact")
	if func():
		exactMatches.append(module)
	return


def findFileInPath(path, file):
	paths = path.split(":")
	for part in paths:
		fullname = part + "/" + file
		try:
			os.stat(fullname)
			return fullname
		except:
			pass
	return None


def findPaths(sysdef, sysinfo, path, bins):
	"""Finds the binaries in the bins map using the path supplied"""
	sysinfo.set("PATH", path)
	for key, val in bins.iteritems():
		sysinfo.set(key, findFileInPath(path, val))
		if not sysinfo.get(key):
			raise cairn.Exception(cairn.ERR_BINARY, "Failed to find required binary: %s" % val)
	return True


def loadModules(root, moduleNames):
	modules = []
	for name in moduleNames:
		fullName = "%s.%s" % (root, name)
		try:
			__import__(fullName)
			modules.append(sys.modules[fullName])
		except ImportError, err:
			raise cairn.Exception(cairn.ERR_MODULE,
								  "Unable to import module '%s'" % fullName)
	return modules
