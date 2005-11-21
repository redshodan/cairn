"""cairn.sysdefs.__init__
   CAIRN System definitions"""


import os
import sys
import re

import cairn
from cairn import Options
from cairn.sysdefs.SystemInfo import *
from cairn.sysdefs import IModule


__sysDef = object()
__sysInfo = SystemInfo()
__sysModuleList = []


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
		return
	import cairn.sysdefs.darwin
	if darwin.matchPlatform():
		cairn.sysdefs.__sysDef = darwin.loadPlatform()
		return
	raise cairn.Exception(cairn.ERR_SYSDEF, "Unable to determine the system definition for this machine.")
	return


def loadModuleList():
	cairn.sysdefs.__sysModuleList = IModule.loadList(cairn.sysdefs.__sysDef)
	return


def run():
	for module in cairn.sysdefs.__sysModuleList:
		if cairn.verbose():
			print "Running module: " + module.__name__
		func = getattr(module, "getClass")
		obj = func()
		if not obj.run(cairn.sysdefs.__sysDef, cairn.sysdefs.__sysInfo):
			raise cairn.Exception("Failed to run module: " + module.__name__)
	return


def printSummary():
	cairn.sysdefs.__sysDef.printSummary();
	cairn.sysdefs.__sysInfo.printSummary();
	return


###
### Utility functions used by sysdef modules.
###

def selectPlatform(root, moduleNames):
	defs = IModule.loadModulesByName(root, moduleNames)

	partialMatches = []
	exactMatches = []
	for module in defs:
		platform = module.getClass()
		verifySysDef(partialMatches, exactMatches, platform)

	# Fall back to "Unknown" if None found
	if len(exactMatches) == 0:
		modules = IModule.loadModulesByName(root, ["unknown"])
		if len(modules) == 1:
			platform = modules[0].getClass()
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


def findPaths(path, bins):
	"""Finds the binaries in the bins map using the path supplied"""
	cairn.sysdefs.__sysInfo.set("PATH", path)
	for key, val in bins.iteritems():
		cairn.sysdefs.__sysInfo.set(key, IModule.findFileInPath(path, val))
		if not cairn.sysdefs.__sysInfo.get(key):
			raise cairn.Exception(cairn.ERR_BINARY, "Failed to find required binary: %s" % val)
	return True
