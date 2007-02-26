"""linux.unknown.setup.PartDevicesParted Module"""


import pylibparted as parted

import cairn
import cairn.sysdefs.templates.unix.restore.setup.PartDevices as tmpl
from cairn.sysdefs.linux import Shared



def getClass():
	return PartDevicesParted()


class PartDevicesParted(tmpl.PartDevices):

	def partitionDevice(self, sysdef, device):
		dev = device.get("mapped-device")
		parts = device.getElems("disk-label/partition")
		try:
			pdev = parted.PedDevice(dev)
			pdtype = parted.PedDiskType(device.get("disk-label/type"))
			pdisk = parted.PedDisk(pdev, pdtype)
			pdisk.delAllPartitions()
			for part in parts:
				type = part.get("type")
				cairn.verbose("partition: %s : %s" % (part.get("device"), type))
				pcon = pdev.getAnyConstraint()
				ppart = parted.PedPartition(pdisk,
											Shared.mapPartType(type),
											None, long(part.get("start")),
											long(part.get("size")) +
											long(part.get("start")))
				ppart.setNum(int(part.get("number")))
				pdisk.addPartition(ppart, pcon)
			pdisk.commit()
			cairn.run("sfdisk -R %s" % dev,
					  "Failed to flush partition table to disk")
		except Exception, err:
			raise cairn.Exception("Failed to write partition table to %s" %
								  dev, err)
		return


	def run(self, sysdef):
		cairn.log("Partitioning devices:")
		for device in sysdef.readInfo.getElems("hardware/device"):
			if ((device.get("status") == "probed") and
				(device.get("type") == "drive")):
				cairn.displayRaw("  %s" % device.get("mapped-device"))
				self.partitionDevice(sysdef, device)
		cairn.displayNL()
		return True
