"""UserShellModule - Container for shell code inputed from the user via the
   command line or config file"""


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
		cairn.run(self.__code, "Failed running user code")
		return True
