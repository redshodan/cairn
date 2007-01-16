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
			command = __builtCmds[sys.argv[1]]
			del sys.argv[1]
		elif (len(sys.argv) >= 2) and (sys.argv[1] == "--version"):
			command = __buildCmds["copy"]
		elif ((len(sys.argv) >= 2) and
			  ((sys.argv[1] == "--help") or (sys.argv[1] == "-h"))):
			return None
	else:
		for key in __builtCmds.keys():
			if cmdname.endswith(key):
				command = __builtCmds[key]
				break
	if not command:
		return None
	subCmds = command.getSubCmds()
	if subCmds and (len(sys.argv) >= 2) and (sys.argv[1] in subCmds.keys()):
			command = subCmds[sys.argv[1]]
			del sys.argv[1]
	return command


def printHelp():
	print "Usage: cairn <command> [command args] ..."
	print "    The command can be one of the following:\n"
	cmds = __builtCmds.keys()
	cmds.sort()
	for key in cmds:
		cmd = __builtCmds[key]
		print "    %s -- %s" % (cmd.name(), cmd.getHelpShortDesc())
	print "\n    Place a '--help' after the command to get that commands help."
	return


def printCmdHelp(command):
	print "Usage: %s" % command.getHelpUsage()
	print "    The sub-command can be one of the following:\n"
	cmds = command.getSubCmds().keys()
	cmds.sort()
	for key in cmds:
		cmd = command.getSubCmds()[key]
		print "    %s -- %s" % (cmd.name(), cmd.getHelpShortDesc())
	print "\n    Place a '--help' after the command to get that commands help."
	return


def run(libname):
	buildCmds(libname)
	command = findCommand()
	if command:
		if command.getModuleString():
			try:
				command.run()
			except Exception, err:
				# The one true catch point for all errors
				if not isinstance(err, exceptions.SystemExit):
					cairn.handleException(err)
			sys.exit(0)
		else:
			printCmdHelp(command)
	else:
		if command != "help":
			print "Invalid command"
			print
		printHelp()
	return
