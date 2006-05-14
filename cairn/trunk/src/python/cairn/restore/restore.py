"""CAIRN Restore Class"""


import sys

import cairn
from cairn import sysdefs
import cairn.Options as Options



class Restore(object):
	def __init__(self):
		return


	def setDefaults():
		Options.getSysInfoOpts()["archive/metafilename"] = \
			"/etc/cairn/cairn-image.xml"
		Options.getSysInfoOpts()["archive/excludes-file"] = \
			"/tmp/excludes"
		return


	def getModuleString(self):
		return "archive.copy;"


	def run(self):
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
		cairn.atexit()
		sys.exit(err.code)
	sys.exit(0)
	return
