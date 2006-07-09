"""CAIRN Restore Class"""


import sys

import cairn
from cairn import sysdefs
import cairn.Options as Options



class Restore(object):

	def setDefaults(self):
		sysdefs.getProgramOpts()["env/mountdir"] = "/mnt/cairn"
		return


	def getModuleString(self):
		return "archive.readmeta; resolve; setup; archive.read; bootloader; cleanup; DisplayDone;"


	def run(self):
		cairn.init()
		Options.set("program", "restore")
		Options.init()
		self.setDefaults()
		Options.parseCmdLineOpts()
		sysdefs.load(self.getModuleString())
		sysdefs.run()
		return


def run():
	try:
		crestore = Restore()
		crestore.run()
	except cairn.Exception, err:
		err.printSelf()
		sys.exit(err.code)
	sys.exit(0)
	return
