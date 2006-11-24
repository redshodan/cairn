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
			cairn.displayRaw("  %s:" % device.get("device").lstrip("/dev/"))
			if device.get("status") != "probed":
				cairn.displayRaw(" No partitions found")
				cairn.displayNL()
				continue
			dev = device.get("device")
			try:
				pdev = parted.PedDevice(dev)
				pdisk = pdev.diskNew()
				pparts = pdisk.getPartitions()
				for ppart in pparts:
					if ppart.getType() & parted.PARTITION_METADATA:
						continue
					pdev = ppart.getPath()
					if not (ppart.getType() & parted.PARTITION_METADATA):
						cairn.displayRaw(" " + ppart.getPath().lstrip("/dev/"))
					pname = "%d" % ppart.getNum()
					part = sysdef.info.createPartitionElem(device, pname)
					if not (ppart.getType() & parted.PARTITION_METADATA):
						part.setChild("device", ppart.getPath())
					Shared.definePartition(sysdef, part, ppart)
				if not len(pparts):
					device.setChild("status", "empty")
					cairn.displayRaw(" No partitions found")
			except Exception, err:
				cairn.displayNL()
				raise cairn.Exception("Failed to read device partitions", err)
			cairn.displayNL()
		return True
