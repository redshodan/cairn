"""linux.unknown.setup.PartDevicesParted Module"""


import pylibparted as parted

import cairn
import cairn.sysdefs.templates.unix.restore.setup.PartDevices as tmpl


def getClass():
	return PartDevicesParted()


class PartDevicesParted(tmpl.PartDevices):

	def partitionDevice(self, sysdef, device):
		dev = device.get("device")
		parts = device.getElems("disk-label/partition")
		try:
			pdev = parted.PedDevice(dev)
			pdisk = parted.PedDisk(pdev, pdev.getType())
			pdisk.delAllPartitions()
			for part in parts:
				pcon = pdev.getAnyConstraint()
				ppart = parted.PedPartition(pdisk,
											self.mapPartType(part.get("type")),
											None, int(part.get("geom.start")),
											int(part.get("geom.size")) +
											int(part.get("geom.start")))
				pdisk.addPartition(part, pcon)
			pdisk.commit()
		except Exception, err:
			raise cairn.Exception("Failed to write partition table to %s" %
								  dev, err)
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
