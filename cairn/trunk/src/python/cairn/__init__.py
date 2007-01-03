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
import time
import re


from types import *
import Options
import Logging
from Logging import critical, error, warn, info, verbose, debug, devel, log, allLog, display, displayRaw, displayNL


# Error codes
ERR_UNKNOWN = 1
ERR_MODULE = 2
ERR_SYSDEF = 3
ERR_BINARY = 4

# Module globals
__file_cleanup = []
__uiCleanUp = None
__start_time = 0
__threads = []



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
	stampStartTime()
	initProcessParams()
	Logging.init()
	debug("Python: %s" % sys.version.replace("\n", ""))
	return


def deinit():
	joinThreads()
	logRunTimeStr()
	return


def stampStartTime():
	global __start_time
	__start_time = time.time()
	return


def getRunTimeStr():
	global __start_time
	delta = int(time.time() - __start_time)
	hours = delta / 3600
	delta = delta % 3600
	mins = delta / 60
	delta = delta % 60
	secs = delta
	hourStr = ""
	if hours: hourStr = "%d hours, " % hours
	minStr = ""
	if mins: minStr = "%d minutes, " % mins
	return "%s%s%d seconds" % (hourStr, minStr, secs)


def logRunTimeStr():
	global __start_time
	if not __start_time:
		return
	if ((Options.get("program") == "extract") or
		(Options.get("program") == "verify")):
		return
	displayNL()
	info("CAIRN ran for %s" % getRunTimeStr())
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


def handleException(err):
	import cairn.sysdefs
	deinit()
	Logging.allLog(Logging.ERROR, "***A FATAL EXCEPTION HAPPENED***")
	if sysdefs and sysdefs.getInfo():
		Logging.allLog(Logging.ERROR, "***META DUMP***\n%s" % 
							 sysdefs.getInfo().toPrettyStr())
	else:
		Logging.allLog(Logging.ERROR, "***META DUMP***\nEmpty meta")
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
	Logging.allLog(Logging.ERROR, "\n".join(msg))
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


# Thread handling
def registerThread(thread):
	global __threads
	__threads.append(thread)
	return


def joinThreads():
	global __threads
	for thr in __threads:
		debug("Stopping thread %s" % thr.getName())
		thr.stop()
		debug("Joining on thread %s" % thr.getName())
		thr.join()
	debug("All threads exited")
	return


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


# Create path to the file if needed
def createFile(filename, mode, desc):
	try:
		path = re.split("/[^/]*$", filename)
		if len(path) > 1:
			info = None
			try:
				info = os.stat(path)
			except:
				pass
			if not info:
				os.makedirs(path[0], 0700)
			elif not stat.S_ISDIR(info[stat.ST_MODE]):
				raise os.error("Path to file %s exists and is not a directory" %
							   filename)
		return file(filename, mode)
	except Exception, err:
		raise cairn.Exception("Failed to open %s file" % desc, err)
	return


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
