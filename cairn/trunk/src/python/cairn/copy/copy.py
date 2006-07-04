"""CAIRN Copy Class"""


import sys

import cairn
from cairn import sysdefs
import cairn.Options as Options



class Copy(object):

	def setDefaults(self):
		sysdefs.getProgramOpts()["archive/metafilename"] = \
			"/etc/cairn/cairn-image.xml"
		sysdefs.getProgramOpts()["archive/excludes-file"] = \
			"/etc/cairn/excludes"
		return


	def getModuleString(self):
		return "archive.write; DisplayDone;"


	def run(self):
		cairn.init()
		Options.set("program", "copy")
		Options.init()
		self.setDefaults()
		Options.parseCmdLineOpts()
		sysdefs.load(self.getModuleString())
		sysdefs.run()
		return


def run():
	try:
		ccopy = Copy()
		ccopy.run()
	except cairn.Exception, err:
		err.printSelf()
		sys.exit(err.code)
	sys.exit(0)
	return
