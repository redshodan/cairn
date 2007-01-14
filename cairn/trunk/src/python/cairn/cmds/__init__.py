"""cairn.cmds"""



import os
import sys


from cairn.cmds import Command
from cairn.cmds import copy
from cairn.cmds import restore
from cairn.cmds import extract
from cairn.cmds import verify


__cmds = {"copy":copy, "restore":restore, "extract":extract, "verify":verify}



def run(libname):
	cmdname = os.path.abspath(sys.argv[0])
	fullCmdLine = " ".join(sys.argv)

	command = None
	if cmdname.endswith("cairn"):
		if (len(sys.argv) >= 2) and (sys.argv[1] in __cmds):
			command = sys.argv[1]
			del sys.argv[1]
		elif (len(sys.argv) >= 2) and (sys.argv[1] == "--version"):
			command = "copy"
		elif ((len(sys.argv) >= 2) and
			  ((sys.argv[1] == "--help") or (sys.argv[1] == "-h"))):
			command = "help"
	else:
		for key in __cmds.keys():
			if cmdname.endswith(key):
				command = key
				break
	if command and (command != "help"):
		klass = __cmds[command].getClass()
		Command.run(klass, libname, fullCmdLine)
	else:
		if command != "help":
			print "Invalid command"
			print
		print "Usage: cairn <command> [command args] ..."
		print "    The command can be one of the following:\n"
		print "    copy  --  Create an image of this computer"
		print "    restore  --  Restore an image to this computer"
		print "    extract  --  Extract files or edit metadata in this image file"
		print "    verify  --  Verify the integrity of this image file\n"
		print "    Place a '--help' after the command to get that commands help."
	return
