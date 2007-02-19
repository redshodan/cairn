"""linux.unknown.restore.setup.MakeFS Module"""



import cairn
from cairn.sysdefs.linux import Constants
import cairn.sysdefs.templates.unix.restore.setup.MakeFS as tmpl


def getClass():
	return MakeFS()


class MakeFS(tmpl.MakeFS):

	def makeFS(self, sysdef, part):
		fsType = part.get("fs/type")
		if not len(fsType) or not part.get("fs/is-normal"):
			return
		if not fsType in Constants.FS_MAP:
			cairn.warn("Skipping unknown filesystem: %s" % fsType)
			return
		tool = sysdef.info.get(Constants.FS_MAP[fsType])
		device = part.get("mapped-device")

		cairn.log("  %s: %s" % (device, fsType))
		args = ""
		if fsType == "reiserfs":
			args = "-ff"
		cmd = "%s %s %s" % (tool, args, device)
		cairn.run(cmd, "Failed to run %s on %s" % (tool, device))
		return


	def run(self, sysdef):
		cairn.log("Creating filesystems")
		for device in sysdef.readInfo.getElems("hardware/device"):
			if device.get("status") == "probed":
				for part in device.getElems("disk-label/partition"):
					self.makeFS(sysdef, part)
		return True
