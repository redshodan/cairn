"""CAIRN runtime options - result of commandline options and config file"""



import getopt
import sys
import re
import string

import cairn


# module globals
ourOpts = {}
ourOptMap = {}

DEFAULT = 0
SHORT = 1
TYPE = 2
SETTER = 3
HELP = 4
STR = 1
BOOL = 2

# module defines
cliCopyHelpHeader = "usage: ccopy [args] file"
cliRestoreHelpHeader = "usage: crestore [args] file"


# Custom opt setters. Have to be here before the opts array.
def setVerboseOpt(opt, arg):
	if get(opt):
		set(opt, get(opt) + 1)
	else:
		set(opt, 1)
	return


# Options and their cmdline arguements are arranged in an array of arrays. Each
# sub-array contains the name of the option, its default value and the short
# cmdline flag for it. The option name will be used for the long form of the
# cmdline flag. The short cmdline flag needs to follow the syntax of the
# getopt package. They will be strung together to make a single string that
# will be passed to getopt. Adding a new entry in the correct option list
# is all that is needed to add in more options.
cliCommonOpts = {
 "modules": [None, "m", STR, None, "List of modules to load."],
 "configfile": [None, "c", STR, None, "Config file to load."],
 "verbose": [False, "v", BOOL, setVerboseOpt,
			 "Verbose operation. Multiple flags will increase verboseness."],
 "force": [False, "f", BOOL, None, "Force operation, ignoring errors."],
 "path": ["/sbin:/bin:/usr/sbin:/usr/bin", None, STR, None,
		  "Path to find programs to run."],
 "help": [False, "h", BOOL, None, None]
}

cliCopyOpts = {"placeholder": [None, None, None, None]}
cliRestoreOpts = {"placeholder": [None, None, None, None]}


def get(name):
	try:
		return ourOpts[name]
	except:
		pass
	return None


def set(name, value):
	ourOpts[name] = value
	return


def init():
	ourOptMap.update(cliCommonOpts)
	if get("program") == "copy":
		ourOptMap.update(cliCopyOpts)
	if get("program") == "restore":
		ourOptMap.update(cliRestoreOpts)
	for opt, row in ourOptMap.iteritems():
		ourOpts[opt] = row[DEFAULT]
	return


def printOpts():
	print "Options:"
	for opt in sorted(ourOpts.keys()):
		print "   %s: %s" % (opt, ourOpts[opt])


def usage():
	if get("program") == "copy":
		print cliCopyHelpHeader, "\n"
		printOptMap()
		sys.exit(0)
	elif get("program") == "restore":
		print cliCopyHelpHeader, "\n"
		printOptMap()
		sys.exit(0)
	else:
		print "Incorrect mode of operation. Can not figure out the program."
		sys.exit(-1)
	return


def printOptMap():
	for name in sorted(ourOptMap.keys()):
		print "  -%s, --%s - %s" % (ourOptMap[name][SHORT], name, ourOptMap[name][HELP])
	return


def parseCmdLineOpts():
	try:
		shortOpts, longOpts = buildOptions(ourOptMap)
		opts, args = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
		parseOpts(opts, args, ourOptMap)
	except getopt.GetoptError, err:
		print err
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


def parseOpts(opts, args, optMap):
	shortIndex = {}
	for name in optMap.keys():
		shortIndex[optMap[name][SHORT]] = name
	for opt, arg in opts:
		opt = string.replace(opt, "-", "")
		if shortIndex.has_key(opt):
			opt = shortIndex[opt]
		if optMap.has_key(opt):
			if optMap[opt][SETTER]:
				optMap[opt][SETTER](opt, arg)
			else:
				defSetter(optMap, opt, arg)
	return


def defSetter(optMap, opt, arg):
	if optMap[opt][TYPE] == STR:
		set(opt, arg)
	else:
		set(opt, True)
	return
