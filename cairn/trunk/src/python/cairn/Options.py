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


def setInfoOpt(opt, arg):
	if (arg.find("=") < 0):
		raise cairn.Exception("Invalid parameter to --set. Must be in the form: key=val")
	words = arg.split("=")
	sysInfoOpts[words[0]] = words[1]
	return


def setMetaFileName(opt, arg):
	set(opt, True)
	sysInfoOpts["archive/metafilename"] = arg
	return


def setHelpOpt(opt, arg):
	usage()
	return


# Options and their cmdline arguements are arranged in an array of arrays. Each
# sub-array contains the name of the option, its default value and the short
# cmdline flag for it. The option name will be used for the long form of the
# cmdline flag. The short cmdline flag needs to follow the syntax of the
# getopt package. They will be strung together to make a single string that
# will be passed to getopt. Adding a new entry in the correct option list
# is all that is needed to add in more options.
cliCommonOpts = {
 "configfile": [None, "c", STR, None, "Config file to load."],
 "dumpmeta": [None, None, STR, setMetaFileName, "Dump the metafile and exit"],
 "force": [False, "f", BOOL, None, "Force operation, ignoring errors."],
 "help": [False, "h", BOOL, setHelpOpt, None],
 "modules": [None, "m", STR, None, "List of modules to load."],
 "path": ["/sbin:/bin:/usr/sbin:/usr/bin", None, STR, None,
		  "Path to find programs to run."],
 "printinfo" : [False, None, BOOL, None, "Print the generated info out."],
 "set": [None, "s", STR, setInfoOpt,
		 "Set a system info option, overriding discovered value"],
 "sysdef": [None, None, STR, None,
			"Manually choose the system definition eg: linux.redhat"],
 "verbose": [False, "v", BOOL, setVerboseOpt,
			 "Verbose operation. Multiple flags will increase verboseness."]
}

cliCopyOpts = {}
cliRestoreOpts = {}
sysInfoOpts = {}


def get(name):
	try:
		return ourOpts[name]
	except:
		pass
	return None


def set(name, value):
	ourOpts[name] = value
	return


def getSysInfoOpts():
	return sysInfoOpts


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
	for opt in ourOptMap.keys():
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
	for name in ourOptMap.keys():
		if ourOptMap[name][SHORT]:
			print "  -%s, --%s - %s" % (ourOptMap[name][SHORT], name,
										ourOptMap[name][HELP])
		else:
			print "  --%s - %s" % (name, ourOptMap[name][HELP])
	return


def parseCmdLineOpts():
	try:
		shortOpts, longOpts = buildOptions(ourOptMap)
		opts, args = getopt.gnu_getopt(sys.argv[1:], shortOpts, longOpts)
		parseOpts(opts, args, ourOptMap)
		ourOptMap.keys().sort()
	except getopt.GetoptError, err:
		print err
		usage()
	return


def buildOptions(optMap):
	shortOpts = [""] * len(optMap)
	longOpts = [None] * len(optMap)
	i = 0
	for name, row in optMap.iteritems():
		if row[TYPE] == STR:
			if row[SHORT]:
				shortOpts[i] = row[SHORT] + ":"
			longOpts[i] = name + "="
		else:
			if row[SHORT]:
				shortOpts[i] = row[SHORT]
			longOpts[i] = name
		i = i + 1
	return string.joinfields(shortOpts, ""), longOpts


def parseOpts(opts, args, optMap):
	shortIndex = {}
	for name in optMap.keys():
		if optMap[name][SHORT]:
			shortIndex[optMap[name][SHORT]] = name
	for opt, arg in opts:
		opt = opt.replace("-", "")
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
