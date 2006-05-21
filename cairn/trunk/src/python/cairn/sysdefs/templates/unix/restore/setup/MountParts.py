"""templates.unix.restore.setup.MountParts Module"""


def getClass():
	return MountParts()


class MountParts(object):

	def orderedList(self, sysdef):
		mountList = []
		fsMap = {}
		for drive in sysdef.info.getElems("hardware/drive"):
			for part in drive.getElems("partition"):
				mountList.append(part.getChild("mount"))
				fsMap[part.getChild("mount")] = part
		mountList.sort()
		return mountList, fsMap


	def run(self, sysdef):
		cairn.log("Mounting filesystems")
		mountList, fsMap = self.orderedList(sysdef)
		self.mountList(sysdef, mountList, fsMap)
		return True
