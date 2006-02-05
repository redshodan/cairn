"""Generic unix.load.Paths system definitions"""


import cairn
import cairn.sysdefs as sysdefs
from cairn import Options


def getClass():
	return Paths()



class Paths(object):

	def __init__(self):
		self.__PATH = ""
		self.__BINS = {"ERROR" : [sysdefs.REQUIRED,
								  "Invalid base function called"]}

	def getPath(self, sysdef):
		if sysdef.info.get("env/path"):
			return sysdef.info.get("env/path")
		return self.__PATH


	def getBins(self, sysdef):
		return self.__BINS


	def chooseTool(self, sysdef, toolType, toolChoices):
		method = None
		userMethod = Options.get(toolType)
		if userMethod:
			for tool in toolChoices:
				if userMethod == tool:
					key = "env/tools/%s" % tool
					if sysdef.info.get(key):
						method = key
					else:
						raise cairn.Exception("%s type %s selected but was not found" % (toolType.capitalize(), tool))
			if not method:
				raise cairn.Exception("Invalid %s type selected: %s" % (toolType, userMethod))
		else:
			method = sysdef.info.get("env/%s-tool" % toolType)
		if method:
			sysdef.info.set("archive/%s-tool" % toolType, method)
		else:
			msg = "No archive types were found. Possible types: "
			for tool in toolChoice:
				msg = msg + tool + ","
			if msg.endswith(","):
				msg = msg[0 : len(msg) - 1]
			raise cairn.Exception(msg)
		return


	def run(self, sysdef):
		sysdefs.findPaths(self.getPath(sysdef), self.getBins(sysdef))
		return True
