"""Module utilities"""


import imp
import sys
import cairn


def loadModules(root, moduleNames):
	modules = []
	for name in moduleNames:
		fullName = "%s.%s" % (root.__name__, name)
		try:
			__import__(fullName)
			modules.append(sys.modules[fullName])
		except ImportError, err:
			raise cairn.Exception(cairn.ERR_MODULE,
								  "Unable to import module %s" % fullName)
	return modules
