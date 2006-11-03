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
		for drive in sysdef.info.getElems("hardware/drive"):
			cairn.displayRaw("  %s:" % drive.get("device").lstrip("/dev/"))
			if drive.get("empty"):
				cairn.displayRaw(" No partitions found")
				cairn.displayNL()
				continue
			device = drive.get("device")
			try:
				pdev = parted.PedDevice(device)
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
						self.definePartition(sysdef, drive, ppart)
				if not foundPart:
					drive.setChild("empty", "True")
					cairn.displayRaw(" No partitions found")
			except Exception, err:
				cairn.displayNL()
				raise cairn.Exception("Failed to partition drive", err)
			cairn.displayNL()
		return True


	def definePartition(self, sysdef, drive, ppart):
		part = sysdef.info.createPartitionElem(drive, "%d" % ppart.getNum())
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
