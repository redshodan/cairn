"""linux.unknown.restore.setup.MountParts Module"""


import os
import os.path
import re
import stat

import cairn
import cairn.sysdefs.templates.unix.restore.setup.MountParts as tmpl
from cairn.sysdefs.linux import Shared


def getClass():
	return MountParts()


class MountParts(tmpl.MountParts):

	def mountParts(self, sysdef, mountList, fsMap):
		mdir = sysdef.info.get("env/mountdir")
		self.mkdir(sysdef, mdir)
		for mount in mountList:
			part = fsMap[mount]
			if (not len(part.get("fs/type")) or
				(part.get("fs/type") == "swap") or
				(part.get("fs/type") == "linux-swap")):
				continue
			fullDir = os.path.join(mdir, mount.lstrip("/"))
			self.mkdir(sysdef, fullDir)
			Shared.mount(sysdef, part.get("mapped-device"), fullDir)
		return


	def mkdir(self, sysdef, dir):
		try:
			info = os.lstat(dir)
			if stat.S_ISDIR(info[stat.ST_MODE]):
				return
		except:
			pass
		cairn.verbose("Making mount directory: %s" % dir)
		try:
			os.makedirs(dir)
		except Exception, err:
			raise cairn.Exception("Failed to create mount dir %s:" % dir, err)
		return
