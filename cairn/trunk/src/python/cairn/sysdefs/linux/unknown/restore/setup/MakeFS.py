"""linux.unknown.restore.setup.MakeFS Module"""


import commands

import cairn
from cairn.sysdefs.linux import Constants
import cairn.sysdefs.templates.unix.restore.setup.MakeFS as tmpl


def getClass():
	return MakeFS()


class MakeFS(tmpl.MakeFS):

	def makeFS(self, sysdef, part):
		fsType = part.getChild("fs-type")
		tool = sysdef.info.get(Constants.FS_MAP[fsType])
		mount = part.getChild("mount")
		device = part.getChild("device")

		cairn.log("  %s: %s" % (device, fsType))
		cmd = "%s %s" % (tool, device)
		ret = commands.getstatusoutput(cmd)
		if ret[0] != 0:
			raise cairn.Exception("Failed to run %s on %s: %s" %
								  (tool, device, ret[1]))
		return fsList


	def run(self, sysdef):
		cairn.log("Creating filesystems")
		for drive in sysdef.info.getElems("hardware/drive"):
			for part in drive.getElems("partition"):
				self.mkfs(sysdef, part)
		return True
