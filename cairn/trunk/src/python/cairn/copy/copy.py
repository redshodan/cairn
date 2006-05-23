"""CAIRN Copy Class"""


import sys

import cairn
from cairn import sysdefs
import cairn.Options as Options



class Copy(object):
	def __init__(self):
		return


	def setDefaults(self):
		Options.getSysInfoOpts()["archive/metafilename"] = \
			"/etc/cairn/cairn-image.xml"
		Options.getSysInfoOpts()["archive/excludes-file"] = \
			"/etc/cairn/excludes"
		return


	def getModuleString(self):
		return "archive.write;"


	def run(self):
		Options.set("program", "copy")
		Options.init()
		self.setDefaults()
		Options.parseCmdLineOpts()
		sysdefs.load(self.getModuleString())
		sysdefs.run()
		cairn.log("Archive finished")
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
