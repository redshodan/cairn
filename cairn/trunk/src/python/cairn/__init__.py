"""CAIRN top level definitions"""


import sys


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
		return


def error(str):
	if Options.get("log") >= ERROR:
		if str:
			print "Error: " + str
		return True
	else:
		return False


def warn(str):
	if Options.get("log") >= WARN:
		if str:
			print "Warning: " + str
		return True
	else:
		return False


def log(str = None, newline = True):
	if Options.get("log") >= LOG:
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
	if Options.get("log") >= VERBOSE:
		if str:
			print str
		return True
	else:
		return False


def debug(str = None):
	if Options.get("log") >= DEBUG:
		if str:
			print str
		return True
	else:
		return False
