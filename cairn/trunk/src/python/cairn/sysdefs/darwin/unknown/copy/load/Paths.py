"""darwin.unknown.copy.load.Paths system definitions"""


import cairn.sysdefs.templates.unix.load.Paths as tmpl



def getClass():
	return Paths()



class Paths(tmpl.Paths):
	def __init__(self):
		self.__PATH = "/sbin:/usr/sbin:/bin:/usr/bin"
		self.__BINS = { "env/part-tool" : "fdisk", "env/archive-tool" : "tar",
						"env/disktool" : "disktool", "env/diskutil" : "diskutil"}
