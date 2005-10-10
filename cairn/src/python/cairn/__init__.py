"""CAIRN top level definitions"""


from types import *


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

