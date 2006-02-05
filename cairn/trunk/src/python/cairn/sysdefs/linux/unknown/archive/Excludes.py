"""linux.archive.Excludes Module"""


import commands

import cairn
from cairn import Options
import cairn.sysdefs.templates.unix.archive.Excludes as tmpl



def getClass():
	return Excludes()


IGNORED_FS = [
	# Pseudo filesystems
	"proc", "sysfs", "tmpfs", "usbfs", "devpts",

	# Network filesystems
	"nfs", "smbfs", "coda",

	# Misc
	"iso9660"
]


class Excludes(tmpl.Excludes):

	def loadFSExcludes(self, sysdef, excludes):
		ret = commands.getstatusoutput(sysdef.info.get("env/tools/mount"))
		if ret[0] != 0:
			raise cairn.Exception("Unable to run mount: %s" % (ret[1]))
		mounts = []
		for line in ret[1].split("\n"):
			lineArr = line.split()
			array = {}
			array[0] = lineArr[0]
			array[1] = lineArr[2]
			array[2] = lineArr[4]
			array[3] = lineArr[5].strip("()")
			mounts.append(array)
		for mount in mounts:
			if ((mount[2] in IGNORED_FS) or (mount[3].find("loop") >= 0) or
				(mount[3].find("bind") >= 0)):
				self.addExcludes(["%s/*" % mount[1]], excludes)
		return
