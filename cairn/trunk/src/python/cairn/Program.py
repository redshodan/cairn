"""cairn.Program - Base program class"""



import sys
import exceptions

import cairn
from cairn import sysdefs
import cairn.Options as Options



class Program(object):

	def __init__(self, libname):
		self._defaults = {}
		self._libname = libname
		return


	def getDefaults(self):
		return self._defaults


	def setDefaults(self):
		return


	def getModuleString(self):
		return ""


	def getLibname(self):
		return self._libname


	def name(self):
		return ""


	def allowBadOpts(self):
		return False


	def run(self):
		cairn.init()
		Options.set("program", self.name())
		Options.init()
		self.setDefaults()
		Options.parseCmdLineOpts(self.allowBadOpts())
		sysdefs.setProgram(self)
		sysdefs.load()
		sysdefs.run()
		return


def run(klass, libname):
	try:
		inst = klass(libname)
		inst.run()
	except Exception, err:
		# The one true catch point for all errors
		if not isinstance(err, exceptions.SystemExit):
			cairn.handleException(err)
	sys.exit(0)
	return
