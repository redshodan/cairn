"""linux.unknown.copy.system.Paths Module"""


import cairn.sysdefs.linux.unknown.system.Paths as tmpl
from cairn.sysdefs.Tools import Tool, ToolGroup


def getClass():
	return Paths()



class Paths(tmpl.Paths):

	def __init__(self):
		super(Paths, self).__init__()
		bins = [ Tool("du", "env/tools/diskusage", True) ]
		self.__BINS = self.__BINS + bins
