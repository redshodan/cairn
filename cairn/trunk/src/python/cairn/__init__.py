"""CAIRN top level definitions"""


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


def debug(str = None):
	if str and Options.get("verbose"):
		print str
		return True
	elif Options.get("verbose"):
		return True
	return False


def verbose(str = None):
	if str and Options.get("verbose"):
		print str
		return True
	elif Options.get("verbose"):
		return True
	return False


def log(str = None):
	if str and Options.get("verbose"):
		print str
		return True
	elif Options.get("verbose"):
		return True
	return False