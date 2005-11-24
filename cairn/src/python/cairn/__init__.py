"""CAIRN top level definitions"""


from types import *
from cairn import Options


# Error codes
ERR_MODULE = 1
ERR_SYSDEF = 2
ERR_BINARY = 3



class Exception(Exception):
	def __init__(self, one, two = None):
		if type(one) is ListType:
			self.code = one[0]
			self.msg = one[1] % two
		else:
			self.code = one
			self.msg = two
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
