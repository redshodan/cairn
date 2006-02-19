"""CAIRN top level definitions"""


import sys


from types import *
from cairn import Options


# Error codes
ERR_UNKNOWN = 1
ERR_MODULE = 2
ERR_SYSDEF = 3
ERR_BINARY = 4



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


def warn(str):
	print "Warning: " + str
	return


def error(str):
	print "Error: " + str
	return


def debug(str = None):
	if Options.get("verbose"):
		if str: print str
		return True
	return False


def verbose(str = None):
	if Options.get("verbose"):
		if str: print str
		return True
	return False


def vverbose(str = None):
	if Options.get("verbose") >= 2:
		if str: print str
		return True
	return False


def vvverbose(str = None):
	if Options.get("verbose") >= 3:
		if str: print str
		return True
	return False


def log(str = None, newline = True):
	if str:
		if newline:
			print str
		else:
			print str,
			sys.stdout.flush()
	return True
