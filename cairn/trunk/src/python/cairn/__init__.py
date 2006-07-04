"""cairn - Top level commonly used definitions"""


import os
import os.path
import stat
import sys
import inspect
import atexit
import logging
import traceback


from types import *
import Logging


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
	Logging.init()
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


def display(msg):
	return Logging.display.log(Logging.INFO, msg)


def displayRaw(msg):
	Logging.all.log(Logging.INFO, msg)
	print msg,
	return


def displayNL():
	print
	return


# Exit and cleanup
def addFileForCleanup(file):
	verbose("Adding file for cleanup at exit: " + file)
	__file_cleanup.append(file)
	return


def cairnAtExit():
	if Options.get("nocleanup"):
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
			error("Failed to delete file: " + file)
	logging.shutdown()
	return

atexit.register(cairnAtExit)
