"""linux.unknown.restore.setup.MountParts Module"""


import commands
import re
import os.path

import cairn
import cairn.sysdefs.templates.unix.restore.setup.MountParts as tmpl


def getClass():
	return MountParts()


class MountParts(tmpl.MountParts):

	def mountList(self, sysdef, mountList, fsMap):
		mdir = sysdef.info.get("env/mountdir")
		self.mkdir(sysdef, mdir)
		for mount in fsList:
			part = fsMap[mount]
			if mount != "/":
				self.mkdir(sysdef, os.path.join(mdir, mount))
		return


	def mkdir(self, sysdef, dir):
		ret = commands.getstatusoutput("mkdir -p %s" % dir)
		if ret[0] != 0:
			raise cairn.Exception("Failed to create mount dir %s: %s" %
								  (dir, ret[1]))
		return
