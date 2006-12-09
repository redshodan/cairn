"""templates.unix.restore.setup.MountParts Module"""


import cairn


def getClass():
	return MountParts()


class MountParts(object):

	def orderedList(self, sysdef):
		mountList = []
		fsMap = {}
		for device in sysdef.readInfo.getElems("hardware/device"):
			if device.get("status") == "probed":
				for part in device.getElems("disk-label/partition"):
					mount = part.get("mount")
					if mount:
						mountList.append(mount)
						fsMap[part.get("mount")] = part
		mountList.sort()
		cairn.verbose("Sorted mounts: %s" % " ".join(mountList))
		return mountList, fsMap


	def mountParts(sysdef, mountList, fsMap):
		raise cairn.Exception("mountParts must be overridden")


	def run(self, sysdef):
		cairn.log("Mounting filesystems")
		mountList, fsMap = self.orderedList(sysdef)
		self.mountParts(sysdef, mountList, fsMap)
		return True
