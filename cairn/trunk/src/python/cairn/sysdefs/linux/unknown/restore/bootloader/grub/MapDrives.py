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
			shutil.move(mapFileName, mapFileName.org)
			mapFile = file(mapFileName, "w+")
		except Exception, err:
			raise cairn.Exception("Failed to open %s: %s" % (mapFileName, err))
		id = 0
		for disk in sysdef.readInfo.getElem("hardware/drive"):
			mapFile.write("(hd%d)  %s" % (id, disk.get("device")))
		mapFile.close()
		return


	def findBootDevice(self, sysdef):
		mountList = []
		fsMap = {}
		for drive in sysdef.readInfo.getElems("hardware/drive"):
			for part in drive.getElems("partition"):
				mountList.append(part.get("mount"))
				fsMap[part.get("mount")] = [drive, part]
		if "/boot" in mountList:
			pair = fsMap["/boot"]
		elif "/" in mountList:
			pair = fsMap["/"]
		else:
			raise cairn.Exception("Could not find the boot partition")


	def run(self, sysdef):
		self.createDeviceMap(sysdef)
		return True
