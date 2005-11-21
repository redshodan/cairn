"""Unknown Darwin system definitions"""


import cairn
import cairn.sysdefs as sysdefs



def getClass():
	return LoadPaths()



class LoadPaths(object):
	def getPath(self):
		return ""


	def getBins(self):
		return {"ERROR" : "Invalid function called"}


	def run(self, sysdef, sysinfo):
		sysdefs.findPaths(self.getPath(), self.getBins())
		return True
