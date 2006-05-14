"""CAIRN top level definitions"""


import os
import stat
import sys
import inspect


from types import *


# Error codes
ERR_UNKNOWN = 1
ERR_MODULE = 2
ERR_SYSDEF = 3
ERR_BINARY = 4

# Log levels
NONE = 0
ERROR = 1
WARN = 2
LOG = 3
VERBOSE = 4
DEBUG = 5

#global __moduleLogMap
__moduleLogMap = {}
__file_cleanup = []


# Have to import Options AFTER log levels are defined
from cairn import Options



class Exception(Exception):
	def __init__(self, msg, code = None):
		self.msg = msg
		if code:
			self.code = code
		else:
			self.code = ERR_UNKNOWN
		return


	def printSelf(self):
		print "Error: %s" % self.msg
		if Options.get("force"):
			print "Force is set, ignoring the previous error"
		return


def setModuleLogLevel(module, level):
	__moduleLogMap[module] = level
	return


def getModuleLogLevel(module):
	return __moduleLogMap[module]


def strToLogLevel(str):
	if str == "error":
		return ERROR
	elif str == "warn":
		return WARN
	elif str == "log":
		return LOG
	elif str == "verbose":
		return VERBOSE
	elif str == "debug":
		return DEBUG
	else:
		return None


def error(str):
	if __getCallers2LogLevel() >= ERROR:
		if str:
			print "Error: " + str
		return True
	else:
		return False


def warn(str):
	if __getCallers2LogLevel() >= WARN:
		if str:
			print "Warning: " + str
		return True
	else:
		return False


def log(str = None, newline = True):
	if __getCallers2LogLevel() >= LOG:
		if str:
			if newline:
				print str
			else:
				print str,
				sys.stdout.flush()
		return True
	else:
		return False


def verbose(str = None):
	if __getCallers2LogLevel() >= VERBOSE:
		if str:
			print str
		return True
	else:
		return False


def debug(str = None):
	if __getCallers2LogLevel() >= DEBUG:
		if str:
			print str
		return True
	else:
		return False


# Only call from a function in this module. It assumes the desired frame to look
# at is 2 above its own frame.
def __getCallers2LogLevel():
	srcFile = inspect.getouterframes(inspect.currentframe())[2][1]
	srcFile = srcFile.replace("/", ".").rstrip(".py")
	for key, val in __moduleLogMap.iteritems():
		if srcFile.endswith(key):
			return val
	return Options.get("log")


def addFileForCleanup(file):
	__file_cleanup.append(file)
	return


def atexit():
	if Options.get("no-cleanup"):
		return
	for file in __file_cleanup:
		try:
			info = os.lstat(file)
			if stat.S_ISDIR(info[stat.ST_MODE]):
				for subfile in os.listdir(file):
					print "os.remove(" + subfile + ")"
				print "os.rmdir(" + file + ")"
			else:
				print "os.remove(" + file + ")"
		except OSError, err:
			error("Failed to delete file: " + file)
	return
