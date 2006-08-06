"""linux.unknown.setup.PartDrivesParted Module"""


import pylibparted as parted

import cairn
import cairn.sysdefs.templates.unix.restore.setup.PartDrives as tmpl


def getClass():
	return PartDrivesParted()


class PartDrivesParted(tmpl.PartDrives):

	def partitionDrive(self, sysdef, drive):
		device = drive.get("device")
		parts = drive.getElems("partition")
		try:
			pdev = parted.PedDevice(device)
			pdisk = parted.PedDisk(pdev, pdev.getType())
			pdisk.delAllPartitions()
			for part in parts:
				pcon = device.getAnyConstraint()
				ppart = parted.PedPartition(pdisk,
											self.mapPartType(part.get("type")),
											None, int(part.get("geom.start")),
											int(part.get("geom.size")) +
											int(part.get("geom.start")))
				pdisk.addPartition(part, pcon)
			pdisk.commit()
		except Exception, err:
			raise cairn.Exception("Failed to write partition table to %s" % device, err)
		return


	def mapPartType(self, type):
		if type == "primary":
			return parted.PARTITION_NORMAL
		elif type == "extended":
			return parted.PARTITION_EXTENDED
		elif type == "logical":
			return parted.PARTITION_LOGICAL
		else:
			raise cairn.Exception("Invalid partition type: %s" % type)
		return
