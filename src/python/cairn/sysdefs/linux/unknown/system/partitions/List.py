"""linux.unknown.system.partitions.List Module"""


import re
import os

import pylibparted as parted

import cairn
import cairn.sysdefs.templates.unix.system.partitions.List as tmpl
from cairn.sysdefs.linux import Shared



def getClass():
	return List()



class List(tmpl.List):

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
				num = 0
				for ppart in pparts:
					pdev = ppart.getPath()
					if ((ppart.getType() & parted.PARTITION_METADATA) or
						(ppart.getType() & parted.PARTITION_FREESPACE)):
						continue
					cairn.displayRaw(" " + ppart.getPath().lstrip("/dev/"))
					part = sysdef.info.createPartitionElem(device, str(num))
					part.setChild("device", ppart.getPath())
					Shared.definePartition(sysdef, part, ppart)
					num = num + 1
				if not len(pparts):
					device.setChild("status", "empty")
					cairn.displayRaw(" No partitions found")
			except Exception, err:
				cairn.displayNL()
				raise cairn.Exception("Failed to read device partitions", err)
			cairn.displayNL()
		return True
