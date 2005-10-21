"""CAIRN Restore Class"""


import sys

import cairn
from cairn import sysdefs 
import cairn.Options as Options



class Restore(object):
	def __init__(self):
		return


	def run(self):
		Options.set("program", "restore")
		Options.init()
		Options.parseCmdLineOpts()
		sysdefs.load()
		sysdefs.run()
		sysdefs.printSummary()
		return

def run():
	try:
		crestore = Restore()
		crestore.run()
	except cairn.Exception, err:
		print "Error: %s" % err.msg
		sys.exit(err.code)
	sys.exit(0)
	return
