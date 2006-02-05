"""CAIRN runtime options - result of commandline options and config file"""



import getopt
import sys
import re
import string

import cairn


# module globals
ourOpts = {}
ourOptMap = {}

# Option value indicies
DEFAULT = 0
SHORT = 1
TYPE = 2
INFO_TAG = 3
SETTER = 4
HELP = 5

# Option types
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


def setExclude(opt, arg):
	optVal = get(opt)
	if optVal:
		set(opt, optVal + ";" + arg)
	else:
		set(opt, arg)
	return


def setInfoOpt(opt, arg):
	if (arg.find("=") < 0):
		raise cairn.Exception("Invalid parameter to --set. Must be in the form: key=val")
	words = arg.split("=")
	sysInfoOpts[words[0]] = words[1]
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
 "configfile" : [None, "c", STR, None, None, "Config file to load."],
 "dumpmeta" : [None, None, STR, "archive/metafilename", None,
			   "Dump the metafile and exit"],
 "exclude" : [None, "x", STR, None, setExclude,
			  "Exclude a file or directory, can specify multiple times"],
 "exclude-from" : [None, "X", STR, "archive/user-excludes-file", None,
				   "File containing exclude directives"],
 "force" : [False, "f", BOOL, None, None, "Force operation, ignoring errors."],
 "help" : [False, "h", BOOL, None, setHelpOpt, None],
 "modules" : [None, "m", STR, None, None, "List of modules to load."],
 "path" : ["/sbin:/bin:/usr/sbin:/usr/bin", None, STR, "env/path", None,
		   "Path to find programs to run."],
 "printmeta" : [False, None, BOOL, None, None, "Print the generated info out."],
 "summary" : [False, None, BOOL, None, None, "Print a summary of generated info."],
 "set" : [None, "s", STR, None, setInfoOpt,
		  "Set a system info option, overriding discovered value"],
 "sysdef" : [None, None, STR, None, None,
			 "Manually choose the system definition eg: linux.redhat"],
 "verbose" : [False, "v", BOOL, None, setVerboseOpt,
			  "Verbose operation. Multiple flags will increase verboseness."]
}

cliCopyOpts = {
 "archive" : ["tar", None, STR, None, None,
			  "Archive type to use: tar, star"],
 "noshar" : [None, None, BOOL, "archive/shar", None,
			 "Create a plain archive without the metadata prepended."],
 "zip" : ["bzip2", None, STR, None, None, "Zip type to use: bzip2, gzip"]
}

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
	keys = ourOptMap.keys()
	keys.sort()
	for name in keys:
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
			if optMap[opt][INFO_TAG]:
				sysInfoOpts[optMap[opt][INFO_TAG]] = arg
			if optMap[opt][SETTER]:
				optMap[opt][SETTER](opt, arg)
			else:
				defSetter(optMap, opt, arg)
	if len(args) == 1:
		set("filename", args[0])
		sysInfoOpts["archive/filename"] = args[0]
	elif len(args) > 1:
		usage()
	return


def defSetter(optMap, opt, arg):
	if optMap[opt][TYPE] == STR:
		set(opt, arg)
	else:
		set(opt, True)
	return
