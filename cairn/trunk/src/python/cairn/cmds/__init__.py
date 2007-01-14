"""cairn.cmds"""



import os
import sys
import exceptions

import cairn
from cairn.cmds import Command
from cairn.cmds import copy, extract, restore, meta, verify


__cmds = [copy, extract, meta, restore, verify]
__builtCmds = {}



def buildCmds(libname):
	fullCmdLine = " ".join(sys.argv)
	for module in __cmds:
		inst = module.getClass()(libname, fullCmdLine)
		__builtCmds[inst.name()] = inst
	return


def findCommand():
	cmdname = os.path.abspath(sys.argv[0])
	command = None
	if cmdname.endswith("cairn"):
		if (len(sys.argv) >= 2) and (sys.argv[1] in __builtCmds.keys()):
			command = sys.argv[1]
			del sys.argv[1]
		elif (len(sys.argv) >= 2) and (sys.argv[1] == "--version"):
			command = "copy"
		elif ((len(sys.argv) >= 2) and
			  ((sys.argv[1] == "--help") or (sys.argv[1] == "-h"))):
			command = "help"
	else:
		for key in __builtCmds.keys():
			if cmdname.endswith(key):
				command = key
				break
	return command


def printHelp():
	print "Usage: cairn <command> [command args] ..."
	print "    The command can be one of the following:\n"
	cmds = __builtCmds.values()
	cmds.sort()
	for cmd in cmds:
		print "    %s -- %s" % (cmd.name(), cmd.getHelpShortDesc())
	print "\n    Place a '--help' after the command to get that commands help."
	return


def run(libname):
	buildCmds(libname)
	command = findCommand()
	if command and (command != "help"):
		try:
			__builtCmds[command].run()
		except Exception, err:
			# The one true catch point for all errors
			if not isinstance(err, exceptions.SystemExit):
				cairn.handleException(err)
		sys.exit(0)
	else:
		if command != "help":
			print "Invalid command"
			print
		printHelp()
	return
