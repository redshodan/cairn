"""cairn.Program - Base program class"""



import sys

import cairn
from cairn import sysdefs
import cairn.Options as Options



class Program(object):

	def __init__(self):
		self._defaults = {}
		return


	def getDefaults(self):
		return self._defaults


	def setDefaults(self):
		return


	def getModuleString(self):
		return ""


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


def run(klass):
	try:
		inst = klass()
		inst.run()
	except Exception, err:
		# The one true catch point for all errors
		cairn.logErr(err)
		sys.exit(1)
	sys.exit(0)
	return