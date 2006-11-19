"""linux.unknown.system.partitions.ListParted Module"""


import re
import os

import pylibparted as parted

import cairn
from cairn.sysdefs.linux import Shared



def getClass():
	return ListParted()


class ListParted(object):

	def run(self, sysdef):
		cairn.log("Checking partitions")
		for device in sysdef.info.getElems("hardware/device"):
			if device.get("type") != "drive":
				continue
			cairn.displayRaw("  %s:" % device.get("device"))
			cairn.displayRaw("  %s:" % device.get("device").lstrip("/dev/"))
			if device.get("empty"):
				cairn.displayRaw(" No partitions found")
				cairn.displayNL()
				continue
			dev = device.get("device")
			try:
				pdev = parted.PedDevice(dev)
				pdisk = pdev.diskNew()
				pparts = pdisk.getPartitions()
				foundPart = False
				for ppart in pparts:
					type = ppart.getType()
					if ((type == parted.PARTITION_NORMAL) or
						(type == parted.PARTITION_LVM) or
						(type == parted.PARTITION_LOGICAL)):
						foundPart = True
						pdev = ppart.getPath()
						cairn.displayRaw(" " + dev.lstrip("/dev/"))
						pname = "%d" % ppart.getNum()
						part = sysdef.info.createPartitionElem(device, pname)
						part.setChild("device", ppart.getPath())
						Shared.definePartition(sysdef, part, ppart)
				if not foundPart:
					device.setChild("empty", "True")
					cairn.displayRaw(" No partitions found")
			except Exception, err:
				cairn.displayNL()
				raise cairn.Exception("Failed to read device partitions", err)
			cairn.displayNL()
		return True
