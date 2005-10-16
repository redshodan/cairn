"""CAIRN Copy Class"""


import sys

import cairn
from cairn import sysdefs 
import cairn.Options



class Copy(object):
	def __init__(self):
		pass
	

	def parseCmdLineArgs(self):
		pass


	def run(self):
		cairn.Options.set("program", "copy")
		cairn.Options.init()
		cairn.Options.parseCmdLineOpts()
		sysdefs.load()
		sysdefs.run()
		sysdefs.printSummary()

def run():
	try:
		ccopy = Copy()
		ccopy.run()
	except cairn.Exception, err:
		print "Error: %s" % err.msg
		sys.exit(err.code)
	sys.exit(0)
