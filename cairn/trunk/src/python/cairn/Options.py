"""CAIRN runtime options - result of commandline options and config file"""


import thirdparty.myoptparse as optparse
import os
import os.path
import platform
import re
import string
import sys
import time
from gettext import gettext as _

import cairn
from cairn import Logging
from cairn import Version


# module globals
__opts = {}
__optMap = {}
__optGroups = {}
__sysInfoOpts = {}
__extraOpts = []


# Opt help levels
COMMON = 0x1
ADVANCED = 0x2
EXPERT = 0x4
DEBUG = 0x8
ALL = COMMON | ADVANCED | EXPERT | DEBUG

helpLevels = [COMMON, ADVANCED, EXPERT, DEBUG]

copyDesc = "Create a CAIRN image of this machine. The image file name is optional. If not specified it will be automatically generated using the machines hostname and todays date. See the description of '--help' for more advanced help options."
copyUsage = "%prog copy [options] [image file]"
restoreDesc = "Restore a CAIRN image onto this machine. See the description of '--help' for more advanced help options."
restoreUsage = "%prog restore [options] <image file>"
extractDesc = "Extract portions of this image file. See the description of '--help' for more advanced help options. This is a frontend to the image tool used to create the image. Any of the options after the -- will be passed on to the image tool. By default this is 'tar'. This can run the image tool without having to extract the image from the CAIRN image file while still exposing virtually all of that image tools funtionality."
extractUsage = "%prog extract [options] <image file> [-- [image tool options]]"
verifyDesc = "Verify the integrity of this image file."
verifyUsage = "%prog verify [options] <image file>"

class Opt(optparse.Option):

	# Filter through the args converting our style to optparse style
	def __init__(self, *args, **kargs):
		self.level = COMMON
		self.info = None
		# is it our style defintion?
		if "cairn" in kargs:
			del kargs["cairn"]
			# Extend with our vars
			if "level" in kargs:
				self.level = kargs["level"]
				del kargs["level"]
			if "info" in kargs:
				self.info = kargs["info"]
				del kargs["info"]
			# Filter
			args = ()
			if "short" in kargs:
				args = args + ("-" + kargs["short"],)
				del kargs["short"]
			else:
				args = args + ("",)
			if "long" in kargs:
				args = args + ("--" + kargs["long"],)
				if ((("action" in kargs) and (kargs["action"] != "callback")) or
					("action" not in kargs)):
					kargs["dest"] = kargs["long"]
				del kargs["long"]
			else:
				raise cairn.Exception("Programming error: option is missing long name")
		optparse.Option.__init__(self, *args, **kargs)
		return


	def take_action(self, action, dest, opt, value, values, parser):
		if self.info:
			setSysInfoOpt(self.info, value)
		return optparse.Option.take_action(self, action, dest, opt, value,
										   values, parser)


# Custom opt setters. Have to be here before the opts array.
def setVerboseOpt(option, opt, value, parser):
	level = get("log")
	if not level:
		set("log", Logging.VERBOSE)
		Logging.setLogLevel(Logging.VERBOSE)
	elif (level > Logging.DEVEL):
		level = level - 10
		set("log", level)
		Logging.setLogLevel(level)
	return


def setLogOpt(option, opt, value, parser):
	if Logging.strToLogLevel(value):
		Logging.setLogLevel(Logging.strToLogLevel(value))
		set("log", Logging.strToLogLevel(value))
	else:
		parser.error("Invalid log level")
	return


def setLogModuleOpt(option, opt, value, parser):
	if value.find("=") <= 0:
		parser.error("Invalid log module specification")
	else:
		arr = value.split("=")
		cairn.setModuleLogLevel(arr[0], cairn.strToLogLevel(arr[1]))
	return


def setLogFileOpt(option, opt, value, parser):
	set("log-file", os.path.abspath(value))
	return


def setExclude(option, opt, value, parser):
	opt = opt.lstrip("-")
	optVal = get("exclude")
	if optVal:
		set("exclude", optVal + ";" + value)
	else:
		set("exclude", value)
	return


def setInfoOpt(option, opt, value, parser):
	if (value.find("=") < 0):
		raise cairn.Exception("Invalid parameter to --set. Must be in the form: key=val")
	words = value.split("=")
	__sysInfoOpts[words[0]] = words[1]
	return


def setSkipDeviceOpt(option, opt, value, parser):
	words = value.split(",")
	cur = ""
	if "archive/skip-devices" in __sysInfoOpts:
		cur = __sysInfoOpts["archive/skip-devices"] + ","
	__sysInfoOpts["archive/skip-devices"] = "%s%s" % (cur, value)
	return


def help(option, opt, value, parser):
	parser.setHelpLevel(COMMON)
	if parser.rargs and len(parser.rargs):
		parser.setHelpLevel(matchSection(parser.rargs[0]))
	parser.print_help()
	sys.exit(0)
	return


def setOpt(option, opt, value, parser):
	if (value.find("=") < 0):
		raise cairn.Exception("Invalid parameter to --set. Must be in the form: key=val")
	words = value.split("=")
	set(words[0], words[1])
	return


def setTmpDirOpt(option, opt, value, parser):
	set("tmpdir", os.path.abspath(value))
	return


def setDestinationOpt(option, opt, value, parser):
	set("destination", os.path.abspath(value))
	return


def setAllFiles(option, opt, value, parser):
	setTmpDirOpt(None, None, value, None)
	setDestinationOpt(None, None, value, None)
	return


def editMetaOpt(option, opt, value, parser):
	arg = nextArgNotOptNotFile(parser)
	if arg:
		set("edit-meta", arg)
	else:
		set("edit-meta", True)
	return


# Options contains the long form, the short form, its type, its default value,
# a system info tag for it to set, a callback function for more complex
# behavior, a help string and a help section. The long name will be used
# for access through set() and get() in this module.
cliCommonOpts = [
	{"long":"dumpenv", "type":"string", "info":"archive/metafilename",
	 "level":EXPERT | DEBUG, "metavar":"ENV-FILE",
	 "help":"Dump the discovered environment information and exit."},
	{"long":"force", "short":"f", "action":"store_true", "level":ADVANCED,
	 "help":"Force operation, ignoring errors."},
	{"long":"help", "short":"h", "action":"callback", "callback":help,
	 "help":"Show this help message. Optionally display one of these help " + \
	 "sections: common, advanced, expert, debug, all. The section name can " + \
	 "be a partial match."},
	{"long":"log", "short":"l", "type":"string", "action":"callback",
	 "default":Logging.INFO, "callback":setLogOpt, "level":ADVANCED | DEBUG,
 	 "help":"Set the logging level: none, error, warn, log (default), " + \
	 "verbose, debug, devel.", "metavar":"LEVEL"},
	{"long":"log-file", "short":"L", "type":"string", "level":ADVANCED | DEBUG,
	 "action":"callback", "callback":setLogFileOpt,
	 "help":"Set the file to log to."},
#	{"long":"log-module", "type":"string", "callback":setLogModuleOpt,
# 	 "help":"Set loglevel for a particular module eg: cairn.sysdefs=debug",
#	 "level":DEBUG, "metavar":"MODULE=LOG-LEVEL"},
	{"long":"modules", "short":"M", "type":"string", "metavar":"MODULE-SPEC",
 	 "help":"Module string which specifies how to adjust the module list.",
	 "level":EXPERT | DEBUG},
	{"long":"no-cleanup", "action":"store_true", "default":False,
 	 "help":"Do not cleanup temporary files.", "level":DEBUG},
	{"long":"no-log", "action":"store_true", "default":False,
 	 "help":"Do not log anything.", "level":ADVANCED},
	{"long":"no-verify", "action":"store_true", "default":False,
 	 "help":"Do not verify metadata or image file.", "level":ADVANCED},
 	{"long":"path", "type":"string", "default":"/sbin:/bin:/usr/sbin:/usr/bin",
 	 "info":"env/path", "level":ADVANCED,
	 "help":"Path to find programs to run."},
 	{"long":"print-opts", "action":"store_true", "default":False, "level":DEBUG,
 	 "help":"Print the command line option values out and exit."},
 	{"long":"print-meta", "action":"store_true", "default":False,
	 "level":DEBUG,
 	 "help":"Print all of the discovered environment information and exit."},
	{"long":"run-modules", "short":"R", "type":"string",
	 "metavar":"MODULE-SPEC", "level":EXPERT | DEBUG,
 	 "help":"Module string which replaces the default module list."},
	{"long":"summary", "action":"store_true", "default":False,
	 "level":ADVANCED | DEBUG,
 	 "help":"Print a summary of the discovered environment information and exit."},
 	{"long":"sysdef", "type":"string", "level":EXPERT,
 	 "help":"Manually choose the system definition eg: linux.redhat"},
	{"long":"tmpdir", "type":"string", "level":ADVANCED,
	 "action":"callback", "callback":setTmpDirOpt, "metavar":"DIR",
	 "help":"Set the location for all temporary files."},
#	{"long":"ui", "type":"string", "level":ADVANCED, "default":"none",
# 	 "help":"Manually choose the user interface: curses, none"},
	{"long":"verbose", "short":"v", "action":"callback",
	 "default":False, "callback":setVerboseOpt,
 	 "help":"Verbose operation. Multiple flags will increase verboseness."},
	{"long":"yes", "short":"y", "action":"store_true", "default":False,
	 "level":ADVANCED | DEBUG, "help":"Automatically answer all questions"}
]

cliCopyRestoreCommonOpts = [
	{"long":"all-files", "type":"string", "level":ADVANCED,
	 "callback":setAllFiles, "metavar":"DIR",
	 "help":"Set the location of all outputed files: temp files, the logfile, and the image file. This is equivalent to calling --tmp, --log-file, --destination with the same directory."},
	{"long":"boot", "short":"B", "type":"string", "level":ADVANCED,
	 "help":"Force this bootloader to be used. Currently supported: grub"},
#	{"long":"configfile", "short":"c", "type":"string", "level":ADVANCED,
#	 "help":"Config file to load."},
	{"long":"destination", "type":"string", "level":ADVANCED, "metavar":"DIR",
	 "action":"callback", "callback":setDestinationOpt,
	 "help":"Set the destination directory for the image file. If no filename was specified then this directory will be used to auto-generate a filename."},
	{"long":"exclude", "short":"x", "type":"string", "action":"callback",
	 "callback":setExclude,
	 "help":"Exclude a file or directory, can specify multiple times."},
	{"long":"exclude-from", "short":"X", "type":"string",
	 "info":"archive/user-excludes-file", "metavar":"FILE",
	 "help":"File containing exclude directives."},
	{"long":"no-lvm", "action":"store_true", "default":False, "level":ADVANCED,
 	 "help":"Do not look for or backup LVM volumes."},
	{"long":"no-raid", "action":"store_true", "default":False, "level":ADVANCED,
 	 "help":"Do not look for or backup software raids."},
	{"long":"no-klog", "action":"store_true", "default":False, "level":ADVANCED,
 	 "help":"Do not log kernel messages."},
	{"long":"setmeta", "type":"string", "callback":setInfoOpt,
	 "level":EXPERT | DEBUG, "metavar":"NAME=VAL",
 	 "help":"Set a system metadata option, overriding discovered value."},
	{"long":"skip", "type":"string", "callback":setSkipDeviceOpt,
	 "level":ADVANCED, "metavar":"device[,device]",
	 "help":"Do not include specified device where device is a full path, '/dev/hda' or device name 'md0'. Automatically excludes mounts from this device."}
]

cliCopyOpts = [
# 	{"long":"archive", "short":"A", "type":"string", "default":"tar",
# 	 "help":"Archive type to use: tar, star", "level":ADVANCED},
 	{"long":"comment", "type":"string", "default":None,
 	 "help":"Add this comment string to the archive file so it can be viewed "
	 "later"},
#	{"long":"noshar", "action":"store_true", "default":False,
#	 "info":"archive/shar", "level":ADVANCED,
# 	 "help":"Create a plain archive without the metadata prepended."},
	{"long":"quick", "short":"q", "action":"store_true", "default":False,
 	 "help":"Skip time consuming steps that are not absolutly needed, eg:" + \
 	 " precise progress meter"},
 	{"long":"zip", "short":"Z", "type":"string", "default":"gzip",
 	 "help":"Zip type to use: bzip2, gzip", "level":ADVANCED}
]

cliRestoreOpts = [
# 	{"long":"archive", "short":"A", "type":"string", "default":"tar",
# 	 "help":"Archive type to use: tar, star", "level":ADVANCED},
 	{"long":"mountdir", "type":"string", "info":"env/mountdir",
 	 "help":"Set the directory to mount restore partitions.", "level":ADVANCED},
	{"long":"pretend", "short":"p", "action":"store_true", "default":False,
	 "help":"Do not do restore, print what actions would happen if restore were to happen."},
	{"long":"quick", "short":"q", "action":"store_true", "default":False,
 	 "help":"Skip time consuming steps that are not absolutly needed, eg:" + \
 	 " precise progress meter"},
 	{"long":"zip", "short":"Z", "type":"string", "default":"gzip",
 	 "help":"Zip type to use: bzip2, gzip", "level":ADVANCED}
]

cliExtractOpts = [
 	{"long":"archive", "short":"A", "type":"string", "default":"tar",
 	 "help":"Archive type to use: tar, star", "level":ADVANCED},
	{"long":"edit-meta", "short":"e", "action":"callback",
	 "callback":editMetaOpt, "metavar":"[EDITOR]",
	 "help":"Run an editor and edit the metadata. After the editor exits the metadata will be saved back to the image. Default editor is $EDITOR."},
	{"long":"preserve", "short":"p", "action":"store_true", "default":False,
	 "help":"Use the same options to the archiver that CAIRN restore would use. These are a number of options for preserving files as faithfully as possible."},
	{"long":"replace-meta", "short":"r", "type":"string", "metavar":"FILE",
	 "help":"Replace the metadata in the image with FILE."},
	{"long":"save-meta", "short":"s", "type":"string", "metavar":"FILE",
	 "help":"Save the metadata to FILE"},
	{"long":"unshar", "short":"u", "type":"string", "metavar":"FILE",
	 "help":"Unshar the image. Removes the metadata placing it in FILE and leaves the bare underlying archive in the image file."}
]

cliVerifyOpts = [
# 	{"long":"archive", "short":"A", "type":"string", "default":"tar",
# 	 "help":"Archive type to use: tar, star", "level":ADVANCED},
#	{"long":"meta", "short":"m", "action":"store_true", "default":False,
#	 "help":"Verify the metadata only. This will perform basic tests on contents of the metadata."},
#	{"long":"archive", "short":"a", "action":"store_true", "default":False,
#	 "help":"Verify the archive only. This will compare the archive md5sum and size to what the metadata has recorded. It will ignore the rest of the metadata"}
]


def get(name):
	try:
		return __opts[name]
	except:
		pass
	return None


def set(name, value):
	__opts[name] = value
	return


def getSysInfoOpts():
	return __sysInfoOpts


def getExtraOpts():
	return __extraOpts


def iterHelpLevels(level):
	ret = []
	for hlevel in helpLevels:
		if hlevel & level:
			ret.append(hlevel)
	return ret


def setSysInfoOpt(option, value):
	__sysInfoOpts[option] = value
	return


def init():
	cairn.allLog(Logging.INFO,
				 "Starting program %s: %s" % (get("program"), " ".join(sys.argv)))
	__sysInfoOpts["archive/cmdline"] = " ".join(sys.argv)
	buildOptMap(cliCommonOpts)
	if get("program") == "copy":
		buildOptMap(cliCopyRestoreCommonOpts)
		buildOptMap(cliCopyOpts)
	if get("program") == "restore":
		buildOptMap(cliCopyRestoreCommonOpts)
		buildOptMap(cliRestoreOpts)
	if get("program") == "extract":
		buildOptMap(cliExtractOpts)
	if get("program") == "verify":
		buildOptMap(cliVerifyOpts)
	return


def buildOptMap(opts):
	for opt in opts:
		__optMap[opt["long"]] = opt
	return


def printAll():
	cairn.display("Option values:")
	keys = __opts.keys()
	keys.sort()
	for key in keys:
		cairn.display("  %s -> %s" % (key, __opts[key]))
	cairn.display("Unknown options:")
	for opt in __extraOpts:
		cairn.display("  %s" % opt)
	cairn.display("System Info Opts:")
	for opt, value in __sysInfoOpts.iteritems():
		cairn.display("  %s -> %s" % (opt, value))
	return


def parseCmdLineOpts(allowBadOpts):
	if get("program") == "copy":
		desc = copyDesc
		usage = copyUsage
	elif get("program") == "restore":
		desc = restoreDesc
		usage = restoreUsage
	elif get("program") == "extract":
		desc = extractDesc
		usage = extractUsage
	elif get("program") == "verify":
		desc = verifyDesc
		usage = verifyUsage
	parser = optparse. \
			 OptionParser(usage=usage, option_class=Opt, prog="cairn",
						  description=desc, title="Common options",
						  conflict_handler="error", add_help_option=False,
						  version=Version.toString(), level=0,
						  error_help="Try 'cairn %s --help'.\n" % \
						  get("program"))
	__optGroups[COMMON] = parser
	__optGroups[ADVANCED] = (parser.
		add_option_group("Advanced options", None, ADVANCED))
	__optGroups[EXPERT] = (parser.
	    add_option_group("Expert options", None, EXPERT))
	__optGroups[DEBUG] = (parser.
	    add_option_group("Debug options", None, DEBUG))

	for name, opt in __optMap.iteritems():
		opt["cairn"] = None
		option = Opt(*(), **opt)
		if ("level" in opt):
			for level in iterHelpLevels(opt["level"]):
				__optGroups[level].add_option(option)
		else:
			__optGroups[COMMON].add_option(option)

	(opts, args) = parser.parse_args()
	for name, val in vars(opts).iteritems():
		if name not in __opts:
			__opts[name] = val

	handleArgs(parser, args, allowBadOpts)
	printOptions()
	return


def handleArgs(parser, args, allowBadOpts):
	dest = get("destination")
	if len(args) == 1:
		filename = checkFileName(args[0])
	elif len(args) == 0:
		if get("program") == "copy":
			filename = checkFileName(generateImageName())
		else:
			parser.error("Missing image filename")
	elif len(args) > 1:
		if allowBadOpts:
			filename = checkFileName(args[0])
			del args[0]
			cairn.Options.__extraOpts = args
		else:
			parser.error("Extra unknown arguments found")

	set("filename", filename)
	__sysInfoOpts["archive/filename"] = filename

	if get("log-file"):
		setLogFile(get("log-file"))
	else:
		if dest:
			setLogFile(os.path.abspath(os.path.join(dest,
							 os.path.basename(filename + ".log"))))
		else:
			setLogFile(filename + ".log")


def checkFileName(filename):
	dest = get("destination")
	if (filename.find("/") >= 0) and dest:
		parser.error("Can not specify --destination and an image file name that is has any directory components in it")
	elif dest:
		filename = os.path.join(dest, filename)
	else:
		filename = os.path.abspath(filename)
	if get("mountdir") and filename.startswith(get("mountdir")):
		parser.error("Can not place the image file underneath the mount directory '%s'" % get("mountdir"))
	return filename


def generateImageName():
	name = "%s-%s.cimg" % (platform.node(), time.strftime("%d-%m-%Y"))
	if get("destination"):
		return os.path.abspath(os.path.join(get("destination"), name))
	else:
		return os.path.abspath(name)


def printOptions():
	if get("print-opts"):
		printAll()
		sys.exit(0)
	return


def matchSection(arg):
	if cairn.matchName("common", arg):
		return COMMON
	elif cairn.matchName("advanced", arg):
		return ADVANCED
	elif cairn.matchName("expert", arg):
		return EXPERT
	elif cairn.matchName("debug", arg):
		return DEBUG
	elif cairn.matchName("all", arg):
		return ALL
	return COMMON


def setLogFile(name):
	if get("no-log"):
		Logging.setLogLevel(Logging.NOLOG)
		return
	set("log-file", name)
	__sysInfoOpts["archive/log-filename"] = name
	Logging.setAllLogFile(name)
	return


def nextArgNotOptNotFile(parser):
	if parser.rargs and len(parser.rargs) and (parser.rargs[0][0] != "-"):
		arg = parser.rargs[0]
		try:
			os.stat(arg)
		except:
			del parser.rargs[0]
			return arg
	return None
