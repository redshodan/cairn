""" cairn.sysdefs.linux.unknown.__init__
	Unknown Linux system definitions"""


import cairn
from cairn import CLoader
from cairn import sysdefs
import cairn.sysdefs.templates.unix as tmpl



def getClass():
	return Unknown()



class Unknown(tmpl.UNIX):
	def __init__(self):
		super(Unknown, self).__init__()
		return


	def name(self):
		return "Unknown"


	def __printSummary(self):
		cairn.log("System definition:  %s Linux" % (self.name()))
		return


	def setup(self):
		import os
		import imp
		import dl
		import stat
		prog = sysdefs.getProgram()
		#name = CLoader.load(prog.getLibname(), "thirdparty", "libuuid.*so.*")
		#os.chmod(name, stat.S_IRWXU)
		#print "name", name
		#print dl.open(name, dl.RTLD_LAZY | dl.RTLD_GLOBAL)
		#name = CLoader.load(prog.getLibname(), "thirdparty", "libparted-.*so.*")
		#os.chmod(name, stat.S_IRWXU)
		#print "name", name
		#print dl.open(name, dl.RTLD_LAZY | dl.RTLD_GLOBAL)
		#name = CLoader.load(prog.getLibname(), "thirdparty", "pylibparted.so")
		name = CLoader.load(prog.getLibname(), "thirdparty", "pylibparted.so")
		os.chmod(name, stat.S_IRWXU)
		#print "name", name
		imp.load_dynamic("pylibparted", name)
		return True
