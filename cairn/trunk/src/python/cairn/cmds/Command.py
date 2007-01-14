"""cairn.cmds.Command"""



import sys
import exceptions

import cairn
from cairn import sysdefs
from cairn import Logging
from cairn import Options



class Command(object):

	def __init__(self, libname, fullCmdLine):
		self._defaults = {}
		self._libname = libname
		self._fullCmdLine = fullCmdLine
		return


	def getDefaults(self):
		return self._defaults


	def setDefaults(self):
		return


	def getModuleString(self):
		return ""


	def getLibname(self):
		return self._libname


	def getFullCmdLine(self):
		return self._fullCmdLine


	def name(self):
		return None


	def getHelpOptMaps(self):
		return None


	def getHelpDesc(self):
		return None


	def getHelpShortdesc(self):
		return None


	def getHelpUsage(self):
		return None


	def allowBadOpts(self):
		return False


	def disableLogging(self):
		return False


	def run(self):
		cairn.init()
		if self.disableLogging():
			Logging.setLogLevel(Logging.NOLOG)
		Options.init(self)
		self.setDefaults()
		Options.parseCmdLineOpts(self.allowBadOpts())
		sysdefs.setCommand(self)
		sysdefs.load()
		sysdefs.run()
		cairn.deinit()
		return
