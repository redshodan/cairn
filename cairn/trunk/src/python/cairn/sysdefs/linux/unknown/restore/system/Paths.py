"""linux.unknown.restore.system.Paths Module"""


import cairn.sysdefs.templates.system.Paths as tmpl
from cairn.sysdefs.Tools import Tool, ToolGroup



def getClass():
	return Paths()



class Paths(tmpl.Paths):
	def __init__(self):
		super(Paths, self).__init__()
		bins = [ Tool("mkfs.ext2", "env/tools/mkfs.ext2", True),
				 Tool("mkfs.ext3", "env/tools/mkfs.ext3", True)
			   ]
		self.__BINS = self.__BINS + bins
