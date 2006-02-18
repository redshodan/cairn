"""CAIRN Copy Class"""


import sys

import cairn
from cairn import sysdefs
import cairn.Options as Options



class Copy(object):
	def __init__(self):
		return


	def run(self):
		Options.set("program", "copy")
		Options.init()
		Options.parseCmdLineOpts()
		sysdefs.load()
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
