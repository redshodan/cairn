#
# CAIRN System definitions
#


import os
import sys
import re

import cairn
from cairn import ModUtils
from cairn.sysdefs.SystemInfo import *


__sysDef = object()
__sysInfo = object()


def getDef():
	return __sysDef


def getInfo():
	return __info


def loadPlatform():
	"""Platform selector"""

	import cairn.sysdefs.linux
	if linux.matchPlatform():
		cairn.sysdefs.__sysDef = linux.loadPlatform()
		cairn.sysdefs.__sysInfo = cairn.sysdefs.__sysDef.loadInfo()
	else:
		raise cairn.Exception(fairn.ERR_SYSDEF, "Unable to determine the system definition for this machine.")


def printSummary():
	cairn.sysdefs.__sysDef.printSummary();
	cairn.sysdefs.__sysInfo.printSummary();



###
### Utility functions used by sysdef modules.
###

def selectPlatform(root, moduleNames):
	defs = ModUtils.loadModules(root, moduleNames)

	partialMatches = []
	exactMatches = []
	for module in defs:
		platform = module.getPlatform()
		verifySysDef(partialMatches, exactMatches, platform)

	# Fall back to "Unknown" if none found
	if len(exactMatches) == 0:
		modules = ModUtils.loadModules(root, ["unknown"])
		if len(modules) == 1:
			platform = modules[0].getPlatform()
			verifySysDef([], [], platform)
			platform.load()
			return platform
		else:
			raise cairn.Exception(cairn.ERR_SYSDEF, "No system definitions match this platform.")
	# Found one, run with it
	if len(exactMatches) == 1:
		exactMatches[0].load()
		return exactMatches[0]
	# Multiple modules think they are right
	elif len(exactMatches) > 1:
		print "There are mutiple system definition matchs:"
		for module in exactMatches:
			print "  ", module.__name__
		raise cairn.Exception(cairn.ERR_SYSDEF, "Multiple system definitions found. Please choose the correct one.")


def verifySysDef(partialMatches, exactMatches, module):
	# Verify contents
	try:
		if (not (getattr(module, "matchPartial") and
				 getattr(module, "matchExact") and
				 getattr(module, "load") and
				 getattr(module, "loadOS") and
				 getattr(module, "loadPaths") and
				 getattr(module, "loadArch") and
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
