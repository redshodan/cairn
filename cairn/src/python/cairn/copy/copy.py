import sys

import cairn
from cairn import sysdefs 
import cairn.Options



class Copy(object):
	#modSet = Set()
	customModList = None


	def __init__(self):
		pass
	

	def parseCmdLineArgs(self):
		pass


	def run(self):
		cairn.Options.set("program", "copy")
		cairn.Options.parseCmdLineOpts()
		sysdefs.loadPlatform()
		sysdefs.printSummary()
		#self.modSet.load(self.customModList)
		#self.modSet.run()


def run():
	try:
		ccopy = Copy()
		ccopy.run()
	except cairn.Exception, err:
		print "Error: %s" % err.msg
		sys.exit(err.code)
	sys.exit(0)
