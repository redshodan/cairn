"""CAIRN Restore Class"""


import sys

import cairn
from cairn import sysdefs
import cairn.Options as Options



class Restore(object):

	def setDefaults(self):
		sysdefs.getProgramOpts()["archive/metafilename"] = \
			"/etc/cairn/cairn-image.xml"
		sysdefs.getProgramOpts()["archive/excludes-file"] = "/tmp/excludes"
		sysdefs.getProgramOpts()["env/mountdir"] = "/mnt/cairn"
		return


	def getModuleString(self):
		return "archive.readmeta; setup; archive.read; bootloader; cleanup;"


	def run(self):
		cairn.init()
		Options.set("program", "restore")
		Options.init()
		self.setDefaults()
		Options.parseCmdLineOpts()
		sysdefs.load(self.getModuleString())
		sysdefs.run()
		cairn.log("Archive restore finished")
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
