"""Unknown Linux system definitions"""


import cairn.sysdefs.templates.unix.LoadPaths as tmpl



def getClass():
	return LoadPaths()



class LoadPaths(tmpl.LoadPaths):
	def __init__(self):
		super(Paths, self).__init__()
		bins_org = self.__BINS
		self.__BINS = { "env/tools/mkfs.ext2" : [sysdefs.PATH_REQUIRED,
												 "mkfs.ext2"],
						"env/tools/mkfs.ext3" : [sysdefs.PATH_REQUIRED,
												 "mkfs.ext3"]
					  }
		self.__BINS.update(bins_org)
