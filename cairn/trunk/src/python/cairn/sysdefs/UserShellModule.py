"""UserShellModule - Container for shell code inputed from the user via the
   command line or config file"""


import commands

import cairn


def getClass(**args):
	if not "code" in args:
		raise cairn.Exception("Missing code parameter to UserModule creation")
	return UserShellModule(**args)



class UserShellModule(object):

	def __init__(self, **args):
		self.__code = args["code"]
		return


	def run(self, sysdef):
		cairn.log("UserShellModule run: " + self.__code)
		ret = commands.getstatusoutput(self.__code)
		if ret[0] != 0:
			raise cairn.Exception("Failed running user code, exit %d: %s" %
								  (ret[0], ret[1]))
		cairn.verbose("UserShellModule output:")
		cairn.verbose(ret[1])
		return True
