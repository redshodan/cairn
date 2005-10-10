"""CAIRN runtime options - result of commandline options and config file"""



import getopt
import sys
import re

import cairn


# module globals
ourOpts = {}
ourDefs = {}


# module defines
cliCopyHelpHeader = "usage: ccopy [args] file"
cliRestoreHelpHeader = "usage: crestore [args] file"

cliCommonHelpArgs = "\
\t-f -- force operation\n\
\t-v -- verbose operation\n\
\t-h, -? -- print this help message\n\
"

cliCommonShortOpts = "c:m:vfC"
cliCommonLongOpts = ["modules", "configfile", "verbose", "force", "continue", "path", "help"]

cliCopyShortOpts = ""
cliCopyLongOpts = []
cliRestoreShortOpts = ""
cliRestoreLongOpts = []


def get(name):
	try:
		return ourOpts[name]
	except:
		pass
	try:
		return ourDefs[name]
	except:
		pass
	return None


def set(name, value):
	ourOpts[name] = value
	return


def init():
	ourDefs["program"] = "unknown"
	ourDefs["configFile"] = None
	ourDefs["verbose"] = False
	ourDefs["force"] = False
	ourDefs["continue"] = False
	ourDefs["path"] = "/sbin:/bin:/usr/sbin:/usr/bin"
	return


def usage():
	if get("program") == "copy":
		print cliCopyHelpHeader, "\n"
		print cliCommonHelpArgs
		sys.exit(0)
	elif get("program") == "restore":
		print cliCopyHelpHeader, "\n"
		print cliCommonHelpArgs
		sys.exit(0)
	else:
		print "Incorrect mode of operation. Can not figure out the program."
		sys.exit(-1)
	return


def parseCmdLineOpts():
	try:
		opts, args = getopt.getopt(sys.argv[1:], cliCommonShortOpts,
								   cliCommonLongOpts)
		parseOpts(opts, args)
		if get("program") == "copy":
			opts, args = getopt.getopt(sys.argv[1:], cliCopyShortOpts,
									   cliCopyLongOpts)
			parseOpts(opts, args)
		elif get("program") == "restore":
			opts, args = getopt.getopt(sys.argv[1:], cliRestoreShortOpts,
									   cliRestoreLongOpts)
			parseOpts(opts, args)
		else:
			print "Internal error. Invalid program type"
			usage()
	except getopt.GetoptError:
		usage()
	return


def parseOpts(opts, args):
	for opt, arg in opts:
		if opt in ("-v", "--verbose"):
			set("verbose", True)
		elif opt in ("-c", "--configfile"):
			set("configFile", arg)
		elif opt in ("--path"):
			set("path", arg)
		elif opt in ("-h", "--help"):
			usage()
	return



init()
