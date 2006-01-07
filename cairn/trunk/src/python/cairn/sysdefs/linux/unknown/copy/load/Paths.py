"""linux.unknown.copy.load.Paths Module"""


import cairn.sysdefs as sysdefs
import cairn.sysdefs.linux.unknown.load.Paths as tmpl



def getClass():
	return Paths()



class Paths(tmpl.Paths):
	def __init__(self):
		super(Paths, self).__init__()
		bins_org = self.__BINS
		self.__BINS = { "env/tools/diskfree" : [sysdefs.PATH_REQUIRED, "df"] }
		self.__BINS.update(bins_org)
