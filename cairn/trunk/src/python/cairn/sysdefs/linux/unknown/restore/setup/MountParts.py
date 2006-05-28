"""linux.unknown.restore.setup.MountParts Module"""


import os
import os.path
import commands
import re
import stat

import cairn
import cairn.sysdefs.templates.unix.restore.setup.MountParts as tmpl


def getClass():
	return MountParts()


class MountParts(tmpl.MountParts):

	def mountList(self, sysdef, mountList, fsMap):
		mdir = sysdef.info.get("env/mountdir")
		self.mkdir(sysdef, mdir)
		for mount in mountList:
			part = fsMap[mount]
			if not len(part.get("fs-type")) or part.get("fs-type") == "swap":
				continue
			fullDir = os.path.join(mdir, mount.lstrip("/"))
			self.mkdir(sysdef, fullDir)
			self.mount(sysdef, part, fullDir)
		return


	def mkdir(self, sysdef, dir):
		try:
			info = os.lstat(dir)
			if stat.S_ISDIR(info[stat.ST_MODE]):
				return
		except:
			pass
		cairn.verbose("Making mount directory: %s" % dir)
		ret = commands.getstatusoutput("mkdir -p %s" % dir)
		if ret[0] != 0:
			raise cairn.Exception("Failed to create mount dir %s: %s" %
								  (dir, ret[1]))
		return


	def mount(self, sysdef, part, fullDir):
		device = part.get("mapped-device")
		cairn.log("Mounting %s on %s" % (device, fullDir))
		ret = commands.getstatusoutput("mount %s %s" % (device, fullDir))
		if ret[0] != 0:
			raise cairn.Exception("Failed to mount %s on %s: %s" %
								  (device, fullDir, ret[1]))
		return
