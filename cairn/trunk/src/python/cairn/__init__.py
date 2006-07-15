"""cairn - Top level commonly used definitions"""


import os
import os.path
import stat
import sys
import atexit
import logging
import traceback
import tempfile


from types import *
import Logging
import Options


# Error codes
ERR_UNKNOWN = 1
ERR_MODULE = 2
ERR_SYSDEF = 3
ERR_BINARY = 4

__file_cleanup = []



# CAIRN base exception. Should be used instead of Pythons base Exception to
# differentiate between std lib errors and CAIRN errors.
class Exception(Exception):
	def __init__(self, msg, code = None):
		self.msg = msg
		if code:
			self.code = code
		else:
			self.code = ERR_UNKNOWN
		return


	def printSelf(self):
		Logging.error.log(Logging.ERROR, "Traceback (most recent call last):")
		for entry in traceback.format_tb(sys.exc_info()[2]):
			Logging.error.log(Logging.ERROR, entry.rstrip())
		error(self.msg)
		if Options.get("force"):
			warn("Force is set, ignoring the previous error")
		return


# Basic initialization function. This really needs to be the first thing done
# in a CAIRN program.
def init():
	checkPythonVer()
	initProcessParams()
	Logging.init()
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
	return Logging.error.log(Logging.CRITICAL, "Critical: " + msg)


def error(msg, *args):
	return Logging.error.log(Logging.ERROR, "Error: " + msg)


def warn(msg, *args):
	return Logging.error.log(Logging.WARNING, "Warning: " + msg)


def info(msg, *args):
	return Logging.display.log(Logging.INFO, msg)


def verbose(msg, *args):
	return Logging.display.log(Logging.VERBOSE, msg)


def debug(msg, *args):
	return Logging.display.log(Logging.DEBUG, msg)


def log(msg, *args):
	return Logging.display.log(Logging.INFO, msg)


def allLog(msg):
	return Logging.all.log(Logging.INFO, msg)


def display(msg):
	return Logging.display.log(Logging.INFO, msg)


def displayRaw(msg):
	Logging.all.log(Logging.INFO, msg)
	print msg,
	sys.stdout.flush()
	return


def displayNL():
	print
	return


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


# Temp files
def mktemp(filename):
	dir = Options.get("tmpdir")
	file = tempfile.mkstemp("", filename, dir)
	addFileForCleanup(file[1])
	return file


# Exit and cleanup
def addFileForCleanup(file):
	verbose("Adding file for cleanup at exit: " + file)
	__file_cleanup.append(file)
	return


def cairnAtExit():
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
