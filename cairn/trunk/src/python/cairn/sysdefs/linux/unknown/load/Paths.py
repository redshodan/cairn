"""linux.unknown.load.Paths Module"""


import cairn.sysdefs as sysdefs
import cairn.sysdefs.templates.unix.load.Paths as tmpl



def getClass():
	return Paths()



class Paths(tmpl.Paths):
	def __init__(self):
		self.__PATH = "/sbin:/usr/sbin:/bin:/usr/bin"
		self.__BINS = { "env/tools/part" : [sysdefs.PATH_REQUIRED, "sfdisk"],
						"env/tools/mount" : [sysdefs.PATH_REQUIRED, "mount"],
						"env/archive-tool" : [sysdefs.PATH_GROUP,
											  {"env/tools/tar" : "tar",
											   "env/tools/star" : "star"}],
						"env/zip-tool" : [sysdefs.PATH_GROUP,
										  {"env/tools/bzip2" : "bzip2",
										   "env/tools/gzip" : "gzip",
										   "env/tools/compress" : "compress"}]
					  }

