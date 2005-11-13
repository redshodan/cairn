"""CAIRN Copy Class"""


import sys

import cairn
from cairn import sysdefs
import cairn.Options as Options



class Copy(object):
	def __init__(self):
		pass


	def run(self):
		Options.set("program", "copy")
		Options.init()
		Options.parseCmdLineOpts()
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
