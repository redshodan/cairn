"""cairn.sysdefs.__init__
   CAIRN System definitions"""


import os
import sys
import re
import inspect

import cairn
from cairn import Options
import cairn.sysdefs.IModule


__sysdef = None
__userCfg = None
__quit = False
__command = None


def getDef():
	global __sysdef
	return __sysdef


def getInfo():
	global __sysdef
	if __sysdef:
		return __sysdef.info
	else:
		return None


def getModuleList():
	global __sysdef
	if __sysdef:
		return __sysdef.moduleList
	else:
		return None


def getCommand():
	global __command
	if __command:
		return __command
	else:
		return None


def setCommand(command):
	cairn.sysdefs.__command = command
	return


def load():
	loadUserConfig()
	loadPlatform()
	loadCommandDefaults()
	loadModuleList()
	verifyModuleList()
	return


def loadUserConfig():
	global __userCfg
	filename = Options.get("configfile")
	if not filename:
		return
	try:
		userCfgFile = file(filename, "rb")
	except Exception, err:
		raise cairn.Exception("Unable to user configfile file %s: %s" % \
							  (filename, err))
	__userCfg = SystemInfo.readNew(userCfgFile)
	userCfgFile.close()
	return


def loadPlatform():
	"""Platform selector"""

	global __sysdef

	userSysdef = Options.get("sysdef")
	if userSysdef:
		words = userSysdef.split(".")
		root = "cairn.sysdefs." + ".".join(words[0:len(words)-1])
		__sysdef = selectPlatform(root, [words[len(words)-1]], True)

	if not __sysdef:
		import cairn.sysdefs.linux
		if linux.matchPlatform():
			__sysdef = linux.loadPlatform()
	if not __sysdef:
		import cairn.sysdefs.darwin
		if darwin.matchPlatform():
			__sysdef = darwin.loadPlatform()
	if not __sysdef:
		raise cairn.Exception("Unable to determine the system definition for this machine.")

	if not __sysdef.init():
		raise cairn.Exception("Unable to initialize the system definition.")
	return


def loadCommandDefaults():
	global __sysdef
	for opt, val in __command.getDefaults().iteritems():
		__sysdef.info.setChild(opt, val)
	return


def loadModuleList():
	global __sysdef
	modList = IModule.ModuleList(__sysdef)
	userModuleSpec = Options.get("modules")
	if Options.get("run-modules"):
		sysmodules = Options.get("run-modules")
	else:
		sysmodules = cairn.sysdefs.__command.getModuleString()
	IModule.loadList(__sysdef, sysmodules, userModuleSpec,
					 modList, None)
	__sysdef.moduleList = modList
	return


def verifyModuleList():
	for modInfo in getModuleList().iter():
		verifyModule(modInfo.module);
	return


def run():
	global __sysdef
	cairn.debug("Final static module list:")
	for name in getModuleList().toStrings():
		cairn.debug("  %s" % name)
	for modInfo in getModuleList().iter():
		if haveQuit():
			cairn.debug("Module requested quit")
			break
		cairn.debug("Running module: " + modInfo.module.__name__)
		try:
			func = getattr(modInfo.module, "getClass")
		except:
			raise cairn.Exception("Module %s does not have a getClass() function" % modInfo.module.__name__)
		# Does it require arguments?
		if inspect.getargspec(func)[2]:
			obj = func(**modInfo.args)
		else:
			obj = func()
		try:
			if not obj.run(__sysdef) and not Options.get("force"):
				raise cairn.Exception("Failed to run module: " +
									  modInfo.module.__name__)
		except cairn.Exception, err:
			if not Options.get("force"):
				raise cairn.Exception("", err)
			else:
				cairn.logErr(err)
				cairn.warn("Force is set, ignoring the previous error")
		getModuleList().next()
	return


def printSummary():
	global __sysdef
	__sysdef.printSummary();
	return


def quit():
	global __quit
	__quit = True
	return


def haveQuit():
	global __quit
	return __quit


###
### Utility functions used by sysdef modules.
###

def selectPlatform(root, moduleNames, force = False):
	defs = IModule.ModuleList(cairn.sysdefs.__sysdef)
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
		modules = IModule.ModuleList(cairn.sysdefs.__sysdef)
		IModule.loadModulesByName(root, ["unknown"], modules)
		if len(modules.iter()) == 1:
			platform = modules.iter()[0].getClass()
			verifySysDef([], [], platform)
			return platform
		else:
			raise cairn.Exception("No system definitions match this platform.")

	# Found one, run with it
	if len(exactMatches) == 1:
		return exactMatches[0]
	# Multiple modules think they are right
	elif len(exactMatches) > 1:
		cairn.error("There are mutiple system definition matchs:")
		for module in exactMatches:
			cairn.error("  %s" % module.__name__)
		raise cairn.Exception("Multiple system definitions found. Please choose the correct one.")
	elif len(exactMatches) < 0:
		raise cairn.Exception("No system definitions match this platform.")
	return


def verifyModule(module):
	try:
		if (not (getattr(module, "getClass"))
			and not cairn.Options.get("continue")):
			raise
	except:
		raise cairn.Exception("Incomplete module %s" % str(module))
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
		raise cairn.Exception("Incomplete system definition code in module %s" %
							  str(module))
	func = getattr(module, "matchPartial")
	if func():
		partialMatches.append(module)
	func = getattr(module, "matchExact")
	if func():
		exactMatches.append(module)
	return
