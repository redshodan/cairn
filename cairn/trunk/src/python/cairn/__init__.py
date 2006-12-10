"""cairn - Top level commonly used definitions"""

import exceptions
import os
import os.path
import stat
import sys
import atexit
import logging
import traceback
import tempfile
import commands


from types import *
import Logging
import Options


# Error codes
ERR_UNKNOWN = 1
ERR_MODULE = 2
ERR_SYSDEF = 3
ERR_BINARY = 4

__file_cleanup = []
__uiCleanUp = None



# CAIRN base exception. Should be used instead of Pythons base Exception to
# differentiate between std lib errors and CAIRN errors.
class Exception(exceptions.Exception):

	def __init__(self, msg, err = None):
		exceptions.Exception.__init__(self, msg)
		self.traces = []
		if err:
			if isinstance(err, Exception):
				self.msgs = [msg] + err.msgs
				self.traces = err.traces
			else:
				self.msgs = [msg, strErr(err)]
			self.traces.append("Traceback (most recent call last):")
			for entry in traceback.format_tb(sys.exc_info()[2]):
				self.traces.append(entry.rstrip())
			self.traces.append(strErr(err))
		else:
			self.msgs = [msg]
		return


	def __str__(self):
		return " ".join(self.msgs)


	def subErrStr(self):
		return self.traces



# Basic initialization function. This really needs to be the first thing done
# in a CAIRN program.
def init():
	checkPythonVer()
	initProcessParams()
	Logging.init()
	debug("Python: %s" % sys.version.replace("\n", ""))
	return


def checkPythonVer():
	if ((sys.version_info[0] < 2) or
		((sys.version_info[0] == 2) and (sys.version_info[1] < 3))):
		print "This version of Python is too old. CAIRN requires version 2.3 or greater to run."
		sys.exit(-1)
	return


def initProcessParams():
	# Close the mask for any files created
	os.umask(077)
	return


# Log pass through functions
def critical(msg, *args):
	return Logging.error.log(Logging.CRITICAL, "Critical: %s" % msg)


def error(msg, *args):
	return Logging.error.log(Logging.ERROR, "Error: %s" % msg)


def warn(msg, *args):
	return Logging.error.log(Logging.WARNING, "Warning: %s" % msg)


def info(msg, *args):
	return Logging.display.log(Logging.INFO, "%s" % msg)


def verbose(msg, *args):
	return Logging.display.log(Logging.VERBOSE, "%s" % msg)


def debug(msg, *args):
	return Logging.display.log(Logging.DEBUG, "%s" % msg)

def devel(msg, *args):
	return Logging.display.log(Logging.DEVEL, "%s" % msg)


def log(msg, *args):
	return Logging.display.log(Logging.INFO, "%s" % msg)


def allLog(msg):
	return Logging.all.log(Logging.INFO, "%s" % msg)


def display(msg):
	return Logging.display.log(Logging.INFO, "%s" % msg)


def displayRaw(msg, dolog = True):
	if dolog:
		Logging.all.log(Logging.INFO, "%s" % msg)
	print msg,
	sys.stdout.flush()
	return


def displayNL():
	print
	return


def handleException(err):
	import cairn.sysdefs
	Logging.all.log(Logging.ERROR, "***A FATAL EXCEPTION HAPPENED***")
	if sysdefs and sysdefs.getInfo():
		Logging.all.log(Logging.ERROR, "***META DUMP***\n%s" % 
						sysdefs.getInfo().prettyStr())
	else:
		Logging.all.log(Logging.ERROR, "***META DUMP***\nEmpty meta")
	logErr(err)
	sys.exit(1)
	return


def logErr(err):
	msg = ["***EXCEPTION***"]
	if isinstance(err, Exception):
		msg = msg + err.subErrStr()
	msg = msg + traceErr(err)
	errmsg = strErr(err)
	msg.append(errmsg)
	Logging.all.log(Logging.ERROR, "\n".join(msg))
	displayNL()
	displayNL()
	error(errmsg)
	return


def traceErr(err):
	msg = []
	msg.append("Traceback (most recent call last):")
	for entry in traceback.format_tb(sys.exc_info()[2]):
		msg.append(entry.rstrip())
	return msg


def strErr(err):
	if isinstance(err, Exception):
		return "%s" % err
	else:
		str = "%s" % err
		if not str or not len(str):
			str = "%s" % err.__class__
			return str.lstrip("exceptions.")
		else:
			return str


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


# Sub process running
def run(cmd, errmsg = None):
	verbose("Running command: %s" % cmd)
	(status, output) = commands.getstatusoutput(cmd)
	verbose("Command output:")
	verbose(output)
	verbose("Command exited with: %d" % status)
	if (status != 0):
		if not errmsg:
			errmsg = "Could not run '%s'" % cmd
		raise Exception("%s: %s" % (errmsg, output))
	return output


# Temp files
def mktemp(filename):
	tmpdir = Options.get("tmpdir")
	file = tempfile.mkstemp("", filename, tmpdir)
	addFileForCleanup(file[1])
	return file


def mkdtemp(filename):
	tmpdir = Options.get("tmpdir")
	dir = tempfile.mkdtemp("", filename, tmpdir)
	addFileForCleanup(dir)
	return dir


# Exit and cleanup
def addFileForCleanup(file):
	verbose("Adding file for cleanup at exit: " + file)
	__file_cleanup.append(file)
	return


def setUICleanUp(func):
	global __uiCleanUp
	__uiCleanUp = func
	return


def cairnAtExit():
	global __uiCleanUp
	if __uiCleanUp:
		try:
			__uiCleanUp()
		except Exception, err:
			logErr(err)
	if Options.get("no-cleanup"):
		return
	for file in __file_cleanup:
		try:
			info = os.lstat(file)
			if stat.S_ISDIR(info[stat.ST_MODE]):
				for subfile in os.listdir(file):
					verbose("Removing: %s" % os.path.join(file, subfile))
					os.remove(os.path.join(file, subfile))
				verbose("Removing: %s" % file)
				os.rmdir(file)
			else:
				verbose("Removing: %s" % file)
				os.remove(file)
		except OSError, err:
			error("Failed to delete file %s: %s" % (file, err))
	logging.shutdown()
	return

atexit.register(cairnAtExit)
