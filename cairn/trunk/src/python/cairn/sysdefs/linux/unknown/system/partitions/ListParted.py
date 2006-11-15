"""linux.unknown.system.partitions.ListParted Module"""


import re
import os

import pylibparted as parted

import cairn


def getClass():
	return ListParted()


class ListParted(object):

	def run(self, sysdef):
		cairn.log("Checking partitions")
		for device in sysdef.info.getElems("hardware/device"):
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
						(type == parted.PARTITION_LOGICAL) or
						(type == parted.PARTITION_LVM) or
						(type == parted.PARTITION_LOGICAL)):
						foundPart = True
						pdev = ppart.getPath()
						cairn.displayRaw(" " + pdev.lstrip("/dev/"))
						self.definePartition(sysdef, device, ppart)
				if not foundPart:
					device.setChild("empty", "True")
					cairn.displayRaw(" No partitions found")
			except Exception, err:
				cairn.displayNL()
				raise cairn.Exception("Failed to read device partitions", err)
			cairn.displayNL()
		return True


	def definePartition(self, sysdef, device, ppart):
		part = sysdef.info.createPartitionElem(device, "%d" % ppart.getNum())
		part.setChild("device", ppart.getPath())
		geom = ppart.getGeometry()
		part.setChild("start", "%ld" % geom.getStart())
		part.setChild("size", "%ld" % geom.getLength())
		if ((ppart.getTypeName() == "gpt") or (ppart.getTypeName() == "mac")):
			part.setChild("label", ppart.getName())
		part.setChild("type", ppart.getTypeName())
		if ppart.isActive():
			part.setChild("active", "true")
		fstype = ppart.getFsType()
		if fstype:
			part.setChild("fs-type", fstype.getName())
		flags = part.getElem("flags")
		for flag in ppart.getFlagsNames():
			flags.createElem("flag", flag)
		return
