"""linux.unknown.restore.bootloader.grub.Tools Module"""


import os.path

import cairn
from cairn.sysdefs.Tools import *



def getClass():
	return Tools()


class Tools(object):

	def __init__(self):
		# The path will have the root mount dir prepended automatically
		self.__PATH = "/sbin:/usr/sbin:/bin:/usr/bin"
		self.__BINS = [Tool("grub", "env/tools/grub", True)]
		return


	def getPath(self, sysdef):
		if sysdef.info.get("env/path"):
			return sysdef.info.get("env/path")
		return self.__PATH


	def getBins(self, sysdef):
		return self.__BINS


	def run(self, sysdef):
		path = self.getPath(sysdef)
		mdir = sysdef.info.get("env/mountdir")
		mpath = ""
		for word in path.split(":"):
			mpath = "%s:%s" % (mpath, os.path.join(mdir, word.lstrip("/")))
		findTools(sysdef, mpath.strip(":"), self.getBins(sysdef))
		return True
