"""Unknown Linux system definitions"""


import cairn.sysdefs.templates.unix.LoadPaths as tmpl



def getClass():
	return LoadPaths()



class LoadPaths(tmpl.LoadPaths):
	def getPath(self):
		return "/sbin:/usr/sbin:/bin:/usr/bin"


	def getBins(self):
		return { "PART_TOOL" : "sfdisk", "ARCHIVE_TOOL" : "tar" }
