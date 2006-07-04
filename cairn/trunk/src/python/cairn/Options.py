"""CAIRN runtime options - result of commandline options and config file"""


import optparse
import os
import re
import string
import sys
from gettext import gettext as _

import cairn
from cairn import Logging
from cairn import Version


# module globals
ourOpts = {}
ourOptMap = {}
ourOptGroups = {}
ourFileRequired = True
sysInfoOpts = {}


# Opt help levels
COMMON = 0x1
ADVANCED = 0x2
EXPERT = 0x4
DEBUG = 0x8
ALL = COMMON | ADVANCED | EXPERT | DEBUG

helpLevels = [COMMON, ADVANCED, EXPERT, DEBUG]

copyDesc = "Create a CAIRN image of this machine."
restoreDesc = "Restore a CAIRN image onto this machine."
helpDesc = " See the description of '--help' for more advanced help options."


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
			sysInfoOpts[self.info] = value
		ret = optparse.Option.take_action(self, action, dest, opt, value,
										  values, parser)
		if ret and (action != "callback") and self.callback:
			args = self.callback_args or ()
			kwargs = self.callback_kwargs or {}
			self.callback(self, opt, value, parser, *args, **kwargs)
		return ret


	def _check_callback(self):
		if self.action == "callback":
			if not callable(self.callback):
				raise OptionError(
					"callback not callable: %r" % self.callback, self)
			if (self.callback_args is not None and
				type(self.callback_args) is not types.TupleType):
				raise OptionError(
					"callback_args, if supplied, must be a tuple: not %r"
					% self.callback_args, self)
			if (self.callback_kwargs is not None and
				type(self.callback_kwargs) is not types.DictType):
				raise OptionError(
					"callback_kwargs, if supplied, must be a dict: not %r"
					% self.callback_kwargs, self)

	CHECK_METHODS = [optparse.Option._check_action,
                     optparse.Option._check_type,
                     optparse.Option._check_choice,
                     optparse.Option._check_dest,
                     optparse.Option._check_const,
                     optparse.Option._check_nargs,
                     _check_callback]



class OptParser(optparse.OptionParser):
	def format_option_help(self, formatter=None):
		if formatter is None:
			formatter = self.formatter
		formatter.store_option_strings(self)
		result = []
		if self.level and (self.level & COMMON) and self.option_list:
			self.option_list = self.sortOptionList(self.option_list)
			result.append(formatter.format_heading(_("common options")))
			formatter.indent()
			result.append(optparse.OptionContainer.
						  format_option_help(self, formatter))
			result.append("\n")
			formatter.dedent()
		for group in self.option_groups:
			if self.level and (self.level & group.level):
				group.option_list = self.sortOptionList(group.option_list)
				result.append(group.format_help(formatter))
				result.append("\n")
		# Drop the last "\n", or the header if no options or option groups:
		return "".join(result[:-1])


	# Allow multiple instances of the same long opt. Useful for showing the
	# same opt in multiple sections
	def _check_conflict(self, option):
		if option._long_opts[0] in self._long_opt:
			return
		else:
			optparse.OptionParser._check_conflict(self, option)
		return

	def error(self, msg):
		self.print_usage(sys.stderr)
		self.exit(2, "%s: error: %s\nTry 'cairn %s --help'.\n" %
				  (self.get_prog_name(), msg, get("program")))


	def sortOptionList(self, list):
		ret = []
		map = {}
		for opt in list:
			map[opt._long_opts[0].lstrip("-")] = opt
		keys = map.keys()
		keys.sort()
		for name in keys:
			ret.append(map[name])
		return ret



class OptGroup(optparse.OptionGroup):
	def __init__(self, parser, title, level):
		self.level = level
		optparse.OptionGroup.__init__(self, parser, title)
		return


	# Allow multiple instances of the same long opt. Useful for showing the
	# same opt in multiple sections
	def _check_conflict(self, option):
		if option._long_opts[0] in self._long_opt:
			return
		else:
			optparse.OptionGroup._check_conflict(self, option)
		return


# Custom opt setters. Have to be here before the opts array.
def setVerboseOpt(option, opt, value, parser):
	level = get("log")
	if not level:
		set("log", Logging.VERBOSE)
	elif (level > Logging.DEBUG):
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


def setExclude(option, opt, value, parser):
	opt = opt.lstrip("-")
	optVal = get("exclude")
	if optVal:
		set("exclude", optVal + ";" + value)
	else:
		set("exclude", value)
	return


def clearFileReq(option, opt, value, parser):
	cairn.Options.ourFileRequired = False
	return


def setInfoOpt(option, opt, value, parser):
	if (value.find("=") < 0):
		raise cairn.Exception("Invalid parameter to --set. Must be in the form: key=val")
	words = value.split("=")
	sysInfoOpts[words[0]] = words[1]
	return


def help(option, opt, value, parser):
	parser.level = COMMON
	if parser.rargs and len(parser.rargs):
		parser.level = matchSection(parser.rargs[0])
	parser.print_help()
	sys.exit(0)
	return


def setOpt(option, opt, value, parser):
	if (value.find("=") < 0):
		raise cairn.Exception("Invalid parameter to --set. Must be in the form: key=val")
	words = value.split("=")
	set(words[0], words[1])
	return


def setLogFileOpt(option, opt, value, parser):
	setLogFile(value)
	return


# Options contains the long form, the short form, its type, its default value,
# a system info tag for it to set, a callback function for more complex
# behavior, a help string and a help section. The long name will be used
# for access through set() and get() in this module.
cliCommonOpts = [
	{"long":"boot", "short":"b", "type":"string", "level":ADVANCED,
	 "help":"Force this bootloader to be used."},
	{"long":"configfile", "short":"c", "type":"string", "level":ADVANCED,
	 "help":"Config file to load."},
	{"long":"dumpmeta", "type":"string", "info":"archive/metafilename",
	 "callback":clearFileReq, "level":EXPERT | DEBUG,
	 "help":"Dump the metafile and exit."},
	{"long":"exclude", "short":"x", "type":"string", "action":"callback",
	 "callback":setExclude,
	 "help":"Exclude a file or directory, can specify multiple times."},
	{"long":"excludefrom", "short":"X", "type":"string",
	 "info":"archive/user-excludes-file",
	 "help":"File containing exclude directives."},
	{"long":"force", "short":"f", "action":"store_true", "level":ADVANCED,
	 "help":"Force operation, ignoring errors."},
	{"long":"help", "short":"h", "action":"callback", "callback":help,
	 "help":"Show this help message. Optionally display one of these help " + \
	 "sections: common, advanced, expert, debug, all. The section name can " + \
	 "be a partial match."},
	{"long":"log", "short":"l", "type":"string", "action":"callback",
	 "default":Logging.INFO, "callback":setLogOpt, "level":ADVANCED | DEBUG,
 	 "help":"Set the logging level: none, error, warn, log (default), " + \
 	 "verbose, debug."},
	{"long":"logfile", "type":"string", "callback":setLogFileOpt,
	 "level":ADVANCED | DEBUG, "help":"Set the file to log to."},
	{"long":"logmodule", "type":"string", "callback":setLogModuleOpt,
 	 "help":"Set loglevel for a particular module eg: cairn.sysdefs=debug",
 	 "level":DEBUG},
	{"long":"metafile", "type":"string", "info":"archive/metafilename",
 	 "help":"Set the metafile name.", "level":EXPERT},
 	{"long":"modules", "short":"m", "type":"string",
 	 "help":"List of modules to load.", "level":EXPERT | DEBUG},
	{"long":"nocleanup", "action":"store_true", "default":False,
 	 "help":"Do not cleanup temporary files.", "level":DEBUG},
 	{"long":"path", "type":"string", "default":"/sbin:/bin:/usr/sbin:/usr/bin",
 	 "info":"env/path", "level":ADVANCED,
	 "help":"Path to find programs to run."},
 	{"long":"printmeta", "action":"store_true", "default":False,
	 "callback":clearFileReq, "level":DEBUG,
 	 "help":"Print the generated info out and exit."},
 	{"long":"printopts", "action":"store_true", "default":False,
	 "callback":clearFileReq, "level":DEBUG,
 	 "help":"Print the command line option values out and exit."},
	{"long":"summary", "action":"store_true", "default":False,
	 "callback":clearFileReq, "level":ADVANCED | DEBUG,
 	 "help":"Print a summary of generated info and exit."},
	{"long":"setmeta", "type":"string", "callback":setInfoOpt,
	 "level":EXPERT | DEBUG,
 	 "help":"Set a system metainfo option, overriding discovered value."},
 	{"long":"sysdef", "type":"string", "level":EXPERT,
 	 "help":"Manually choose the system definition eg: linux.redhat"},
	{"long":"verbose", "short":"v", "action":"callback",
	 "default":False, "callback":setVerboseOpt,
 	 "help":"Verbose operation. Multiple flags will increase verboseness."}
]

cliCopyOpts = [
 	{"long":"archive", "short":"a", "type":"string", "default":"tar",
 	 "help":"Archive type to use: tar, star", "level":ADVANCED},
	{"long":"noshar", "action":"store_true", "default":False,
	 "info":"archive/shar", "level":ADVANCED,
 	 "help":"Create a plain archive without the metadata prepended."},
	{"long":"quick", "short":"q", "action":"store_true", "default":False,
 	 "help":"Skip time consuming steps that are not absolutly needed, eg:" + \
 	 " precise progress meter"},
 	{"long":"zip", "short":"z", "type":"string", "default":"gzip",
 	 "help":"Zip type to use: bzip2, gzip", "level":ADVANCED}
]

cliRestoreOpts = [
 	{"long":"archive", "short":"a", "type":"string", "default":"tar",
 	 "help":"Archive type to use: tar, star", "level":ADVANCED},
 	{"long":"mountdir", "type":"string", "info":"env/mountdir",
 	 "help":"Set the directory to mount restore partitions.", "level":ADVANCED},
	{"long":"quick", "short":"q", "action":"store_true", "default":False,
 	 "help":"Skip time consuming steps that are not absolutly needed, eg:" + \
 	 " precise progress meter"},
 	{"long":"zip", "short":"z", "type":"string", "default":"gzip",
 	 "help":"Zip type to use: bzip2, gzip", "level":ADVANCED}
]


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


def iterHelpLevels(level):
	ret = []
	for hlevel in helpLevels:
		if hlevel & level:
			ret.append(hlevel)
	return ret


def init():
	buildOptMap(cliCommonOpts)
	if get("program") == "copy":
		buildOptMap(cliCopyOpts)
	if get("program") == "restore":
		buildOptMap(cliRestoreOpts)
	return


def buildOptMap(opts):
	for opt in opts:
		ourOptMap[opt["long"]] = opt
	return


def printAll():
	cairn.display("Option values:")
	for key, val in ourOpts.iteritems():
		cairn.display("  %s -> %s" % (key, val))
	return


def parseCmdLineOpts():
	if get("program") == "copy":
		desc = copyDesc
	elif get("program") == "restore":
		desc = restoreDesc
	usage = "%prog " + "%s [options] file" % get("program")
	parser = OptParser(usage=usage, option_class=Opt,
					   prog="cairn", description=desc + helpDesc,
					   conflict_handler="error", add_help_option=False,
					   version=Version.toString())
	ourOptGroups[COMMON] = parser
	ourOptGroups[ADVANCED] = (parser.
		add_option_group(OptGroup(parser, "advanced options", ADVANCED)))
	ourOptGroups[EXPERT] = (parser.
	    add_option_group(OptGroup(parser, "expert options", EXPERT)))
	ourOptGroups[DEBUG] = (parser.
	    add_option_group(OptGroup(parser, "debug options", DEBUG)))

	for name, opt in ourOptMap.iteritems():
		opt["cairn"] = None
		option = Opt(*(), **opt)
		if ("level" in opt):
			for level in iterHelpLevels(opt["level"]):
				ourOptGroups[level].add_option(option)
		else:
			ourOptGroups[COMMON].add_option(option)

	(opts, args) = parser.parse_args()
	for name, val in vars(opts).iteritems():
		if name not in ourOpts:
			ourOpts[name] = val

	if len(args) == 1:
		str = os.path.abspath(args[0])
		set("filename", str)
		sysInfoOpts["archive/filename"] = str
		if not get("logfile"):
			setLogFile(str + ".log")
	elif len(args) > 1:
		parser.error("Missing filename")
	elif (len(args) == 0) and ourFileRequired:
		parser.error("Missing filename")
	return


def matchSection(arg):
	if matchName("common", arg):
		return COMMON
	elif matchName("advanced", arg):
		return ADVANCED
	elif matchName("expert", arg):
		return EXPERT
	elif matchName("debug", arg):
		return DEBUG
	elif matchName("all", arg):
		return ALL
	return COMMON


def matchName(name, arg):
	if not arg or not len(arg):
		return False
	nlen = len(name)
	alen = len(arg)
	index = 0
	while ((index < nlen) and (index < alen)):
		if name[index] != arg[index]:
			break
		index = index + 1
	if ((index == nlen) or (index == alen)):
		return True
	else:
		return False


def setLogFile(name):
	set("logfile", name)
	sysInfoOpts["archive/log-filename"] = name
	Logging.setAllLogFile(name)
	return
