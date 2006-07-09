"""templates.unix.restore.setup.MountParts Module"""


import cairn


def getClass():
	return MountParts()


class MountParts(object):

	def orderedList(self, sysdef):
		mountList = []
		fsMap = {}
		for drive in sysdef.readInfo.getElems("hardware/drive"):
			if not drive.get("empty"):
				for part in drive.getElems("partition"):
					mountList.append(part.get("mount"))
					fsMap[part.get("mount")] = part
		mountList.sort()
		return mountList, fsMap


	def run(self, sysdef):
		cairn.log("Mounting filesystems")
		mountList, fsMap = self.orderedList(sysdef)
		self.mountList(sysdef, mountList, fsMap)
		return True
