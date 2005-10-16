"""CAIRN runtime options - result of commandline options and config file"""



import getopt
import sys
import re
import string

import cairn


# module globals
ourOpts = {}
ourDefs = {}

DEFAULT = 0
SHORT = 1
TYPE = 2
HELP = 3
STR = 1
BOOL = 2

# module defines
cliCopyHelpHeader = "usage: ccopy [args] file"
cliRestoreHelpHeader = "usage: crestore [args] file"

# Options and their cmdline arguements are arranged in an array of arrays. Each sub-array
# contains the name of the option, its default value and the short cmdline flag for it. The
# option name will be used for the long form of the cmdline flag. The short cmdline flag
# needs to follow the syntax of the getopt package. They will be strung together to make
# a single string that will be passed to getopt. Adding a new entry in the correct option list
# is all that is needed to add in more options.
cliCommonOpts = {
 "modules": [None, "m", STR, "List of modules to load"],
 "configfile": [None, "c", STR, "Config file to load"],
 "verbose": [False, "v", BOOL, "Verbose operation"],
 "force": [False, "f", BOOL, "Force operation, ignoring errors"],
 "path": ["/sbin:/bin:/usr/sbin:/usr/bin", None, STR, "Path to find programs to run"],
 "help": [None, None, None, None]
}

cliCopyOpts = {}
cliRestoreOpts = {}


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
	optMap = {}
	optMap.update(cliCommonOpts)
	if get("program") == "copy":
		print cliCopyHelpHeader, "\n"
		optMap.update(cliCopyOpts)
		printOptMap(optMap)
		sys.exit(0)
	elif get("program") == "restore":
		print cliCopyHelpHeader, "\n"
		optMap.update(cliRestoreOpts)
		printOptMap(optMap)
		sys.exit(0)
	else:
		print "Incorrect mode of operation. Can not figure out the program."
		sys.exit(-1)
	return


def printOptMap(optMap):
	for name in sorted(optMap.keys()):
		print "  -%s, --%s - %s" % (optMap[name][SHORT], name, optMap[name][HELP])
	return


def parseCmdLineOpts():
	try:
		shortOpts, longOpts = buildOptions(cliCommonOpts)
		opts, args = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
		parseOpts(opts, args)
		if get("program") == "copy":
			shortOpts, longOpts = buildOptions(cliCopyOpts)
			opts, args = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
			parseOpts(opts, args)
		elif get("program") == "restore":
			shortOpts, longOpts = buildOptions(cliRestoreOpts)
			opts, args = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
			parseOpts(opts, args)
		else:
			print "Internal error. Invalid program type"
			usage()
	except getopt.GetoptError:
		usage()
	return


def buildOptions(optMap):
	shortOpts = [""] * len(optMap)
	longOpts = [None] * len(optMap)
	i = 0
	for name, row in optMap.iteritems():
		if row[SHORT]:
			if row[TYPE] == STR:
				shortOpts[i] = row[SHORT] + ":"
			else:
				shortOpts[i] = row[SHORT]
		longOpts[i] = name
		i = i + 1
	return string.joinfields(shortOpts, ""), longOpts


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



#init()
