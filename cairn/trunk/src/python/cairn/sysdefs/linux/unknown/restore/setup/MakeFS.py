"""linux.unknown.restore.setup.MakeFS Module"""


import commands

import cairn
from cairn.sysdefs.linux import Constants
import cairn.sysdefs.templates.unix.restore.setup.MakeFS as tmpl


def getClass():
	return MakeFS()


class MakeFS(tmpl.MakeFS):

	def makeFS(self, sysdef, part):
		fsType = part.get("fs-type")
		if not len(fsType):
			return
		tool = sysdef.info.get(Constants.FS_MAP[fsType])
		device = part.get("mapped-device")

		cairn.log("  %s: %s" % (device, fsType))
		cmd = "%s %s" % (tool, device)
		ret = commands.getstatusoutput(cmd)
		if ret[0] != 0:
			raise cairn.Exception("Failed to run %s on %s: %s" %
								  (tool, device, ret[1]))
		cairn.verbose(ret[1])
		return


	def run(self, sysdef):
		cairn.log("Creating filesystems")
		for device in sysdef.readInfo.getElems("hardware/device"):
			if not device.get("empty"):
				for part in device.getElems("device-label/partition"):
					self.makeFS(sysdef, part)
		return True
