"""UserModule - Container for code inputed from the user via the command line
   or config file"""


import os
import os.path
import stat
import commands
import shutil

import cairn


def getClass(**args):
	if not "code" in args:
		raise cairn.Exception("Missing code parameter to UserModule creation")
	return UserModule(**args)



class UserModule(object):

	def __init__(self, **args):
		self.__code = args["code"]
		return


	def run(self, sysdef):
		cairn.log("UserModule run: " + self.__code)
		try:
			ret = False
			#objCode = compile("def func():\n" + self.__code + "\nret=func()\n", "UserModule", 'exec')
			objCode = compile(self.__code + "\n", "UserModule", 'exec')
			exec objCode
			return ret
		except Exception, err:
			raise cairn.Exception("Failed running user code", err)
		return False
