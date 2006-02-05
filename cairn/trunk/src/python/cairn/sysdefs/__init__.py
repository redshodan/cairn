"""cairn.sysdefs.__init__
   CAIRN System definitions"""


import os
import sys
import re

import cairn
from cairn import Options
import cairn.sysdefs.IModule


__sysdef = object()


PATH_GROUP = 0
PATH_OPTIONAL = 1
PATH_REQUIRED = 2


def getDef():
	return __sysdef


def getInfo():
	return __sysdef.info


def getModuleList():
	return __sysdef.moduleList


def load():
	loadPlatform()
	loadModuleList()
	verifyModuleList()
	return


def loadPlatform():
	"""Platform selector"""

	import cairn.sysdefs
	userSysdef = Options.get("sysdef")
	if userSysdef:
		words = userSysdef.split(".")
		root = ".".join(words[0:len(words)-1])
		cairn.sysdefs.__sysdef = selectPlatform(root, [words[len(words)-1]], True)
		return

	import cairn.sysdefs.linux
	if linux.matchPlatform():
		cairn.sysdefs.__sysdef = linux.loadPlatform()
		return
	import cairn.sysdefs.darwin
	if darwin.matchPlatform():
		cairn.sysdefs.__sysdef = darwin.loadPlatform()
		return
	raise cairn.Exception("Unable to determine the system definition for this machine.",
						  cairn.ERR_SYSDEF)
	return


def loadModuleList():
	modules = IModule.ModuleList()
	userModuleSpec = Options.get("modules")
	IModule.loadList(cairn.sysdefs.__sysdef, cairn.sysdefs.__sysdef.getModuleString(),
					 userModuleSpec, modules, None)
	cairn.sysdefs.__sysdef.moduleList = modules
	return


def verifyModuleList():
	for module in getModuleList().iter():
		verifyModule(module);
	return


def run():
	cairn.verbose("Final module list: " + getModuleList().toString())
	for module in getModuleList().iter():
		cairn.verbose("Running module: " + module.__name__)
		try:
			func = getattr(module, "getClass")
		except:
			raise cairn.Exception("Module %s does not have a getClass() function" % module.__name__)
		obj = func()
		if not obj.run(cairn.sysdefs.__sysdef):
			raise cairn.Exception("Failed to run module: " + module.__name__)
		getModuleList().next()
	return


def printSummary():
	cairn.sysdefs.__sysdef.printSummary();
	return


###
### Utility functions used by sysdef modules.
###

def selectPlatform(root, moduleNames, force = False):
	defs = IModule.ModuleList()
	IModule.loadModulesByName(root, moduleNames, defs)

	partialMatches = []
	exactMatches = []
	for module in defs.iter():
		platform = module.getClass()
		verifySysDef(partialMatches, exactMatches, platform)
		# Forcing a sysdef, ignore what the module thinks.
		if force:
			return platform

	# Fall back to "Unknown" if None found
	if len(exactMatches) == 0:
		modules = IModule.ModuleList()
		IModule.loadModulesByName(root, ["unknown"], modules)
		if len(modules.iter()) == 1:
			platform = modules.iter()[0].getClass()
			verifySysDef([], [], platform)
			return platform
		else:
			raise cairn.Exception("No system definitions match this platform.",
								  cairn.ERR_SYSDEF)

	# Found one, run with it
	if len(exactMatches) == 1:
		return exactMatches[0]
	# Multiple modules think they are right
	elif len(exactMatches) > 1:
		print "There are mutiple system definition matchs:"
		for module in exactMatches:
			print "  ", module.__name__
		raise cairn.Exception("Multiple system definitions found. Please choose the correct one.", cairn.ERR_SYSDEF)
	elif len(exactMatches) < 0:
		raise cairn.Exception("No system definitions match this platform.",
							  cairn.ERR_SYSDEF)
	return


def verifyModule(module):
	try:
		if (not (getattr(module, "getClass"))
			and not cairn.Options.get("continue")):
			raise
	except:
		raise cairn.Exception("Incomplete module " + str(module), cairn.ERR_SYSDEF)
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
		raise cairn.Exception("Incomplete system definition code in module " +
							  str(module), cairn.ERR_SYSDEF)
	func = getattr(module, "matchPartial")
	if func():
		partialMatches.append(module)
	func = getattr(module, "matchExact")
	if func():
		exactMatches.append(module)
	return


def findPaths(path, bins):
	"""Finds the binaries in the bins map using the path supplied"""
	getInfo().set("env/path", path)
	for key, arr in bins.iteritems():
		if (arr[0] == PATH_REQUIRED) or (arr[0] == PATH_OPTIONAL):
			getInfo().set(key, IModule.findFileInPath(path, arr[1]))
		elif arr[0] == PATH_GROUP:
			first = None
			for subkey, name in arr[1].iteritems():
				bin = IModule.findFileInPath(path, name)
				if bin:
					getInfo().set(subkey, bin)
					if not first:
						first = subkey
				else:
					getInfo().set(subkey, "")
			if first:
				getInfo().set(key, first)
		# Verify it was found
		if not getInfo().get(key):
			raise cairn.Exception("Failed to find required binary: %s" % val,
								  cairn.ERR_BINARY)
	return True
