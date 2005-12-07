"""Unknown Linux system definitions"""


import cairn.sysdefs.templates.unix.LoadPaths as tmpl



__PATH = "/sbin:/usr/sbin:/bin:/usr/bin"
__BINS = { "env/part-tool" : "sfdisk", "env/archive-tool" : "tar" }



def getClass():
	return LoadPaths()



class LoadPaths(tmpl.LoadPaths):
	def getPath(self):
		return __PATH


	def getBins(self):
		return __BINS
