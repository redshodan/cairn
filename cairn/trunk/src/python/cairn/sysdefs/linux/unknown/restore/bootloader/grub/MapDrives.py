"""linux.unknown.restore.bootloader.grub.MapDrives Module"""


import os.path
import shutil

import cairn



def getClass():
	return MapDrives()


class MapDrives(object):

	def createDeviceMap(self, sysdef):
		mdir = sysdef.info.get("env/mountdir")
		mapFileName = os.path.join(mdir, "boot/grub/device.map")
		mapFile = None
		try:
			shutil.move(mapFileName, mapFileName + ".org")
		except Exception, err:
			pass
		try:
			mapFile = file(mapFileName, "w+")
		except Exception, err:
			raise cairn.Exception("Failed to open %s: %s" % (mapFileName, err))
		id = 0
		for disk in sysdef.readInfo.getElems("hardware/drive"):
			mapFile.write("(hd%d)  %s" % (id, disk.get("device")))
		mapFile.close()
		return


	def findBootDevice(self, sysdef):
		mountList = []
		fsMap = {}
		driveID = -1
		partID = -1
		for drive in sysdef.readInfo.getElems("hardware/drive"):
			driveID = driveID + 1
			for part in drive.getElems("partition"):
				partID = partID + 1
				mountList.append(part.get("mount"))
				fsMap[part.get("mount")] = [drive, driveID, part, partID]
		if "/boot" in mountList:
			tuple = fsMap["/boot"]
		elif "/" in mountList:
			tuple = fsMap["/"]
		else:
			raise cairn.Exception("Could not find the boot partition")
		cairn.debug("machine/bootloader/drive: (hd%d)" % tuple[1])
		cairn.debug("machine/bootloader/drive-os: %s" % tuple[0].get("device"))
		cairn.debug("machine/bootloader/partition: (hd%d,%d)" %
					(tuple[1], tuple[3]))
		cairn.debug("machine/bootloader/partition-os: %s", tuple[2].get("device"))
		sysdef.info.setChild("machine/bootloader/drive", "(hd%d)" % tuple[1])
		sysdef.info.setChild("machine/bootloader/drive-os", tuple[0].get("device"))
		sysdef.info.setChild("machine/bootloader/partition",
							 "(hd%d,%d)" % (tuple[1], tuple[3]))
		sysdef.info.setChild("machine/bootloader/partition-os",
							 tuple[2].get("device"))
		return


	def run(self, sysdef):
		self.createDeviceMap(sysdef)
		self.findBootDevice(sysdef)
		return True
