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

	###
	### Help related functions
	###

	def getHelpOptMaps(self):
		return None


	def getHelpDesc(self):
		return None


	def getHelpShortdesc(self):
		return None


	def getHelpUsage(self):
		return None


	###
	### Runtime related functions
	###

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


	def disableLogging(self):
		return False


	def name(self):
		return None


	def fullName(self):
		name = self.name()
		cmd = self
		while cmd.parent():
			cmd = cmd.parent()
			name = "%s %s" % (cmd.name(), name)
		return name


	def parent(self):
		return None


	###
	### Command line parsing functions
	###

	def allowBadOpts(self):
		return False


	def getOptMaps(self):
		return ()


	def getSubCmds(self):
		return None


	# This is the real 'main()' of CAIRN.
	def run(self):
		cairn.init()
		if self.disableLogging():
			Logging.setLogLevel(Logging.NOLOG)
		Options.init(self)
		self.setDefaults()
		Options.parseCmdLineOpts(self.allowBadOpts())
		cairn.initPostOpts()
		sysdefs.setCommand(self)
		sysdefs.load()
		sysdefs.run()
		cairn.deinit()
		return
