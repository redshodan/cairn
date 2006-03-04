"""darwin.unknown.hardware.Partitions Module"""


import os
import commands
import re

import cairn
import cairn.sysdefs.templates.unix.hardware.Partitions as tmpl


def getClass():
	return Partitions()


class Partitions(tmpl.Partitions):
	def run(self, sysdef):
		for drive in sysdef.info.getElems("hardware/drive"):
			self.definePartitions(sysdef, drive)
		return True


	def definePartitions(self, sysdef, drive):
		ret = commands.getstatusoutput("%s list %s" % (sysdef.info.get("env/tools/diskutil"), drive.instName()))
		if ret[0] != 0:
			msg = "Failed to run %s to find drive information:\n" % sysdef.info.get("env/tools/diskutil")
			raise cairn.Exception(msg + ret[1])
		partNum = 1
		for line in ret[1].split("\n"):
			arr = line.split()
			if (arr[0] != "0:") and re.match("[0-9]*:", arr[0]):
				part = sysdef.info.createPartitionElem(drive, "%d" % partNum)
				part.setChild("device", "/dev/" + arr[len(arr) - 1])
				part.setChild("label", " ".join(arr[2:len(arr) - 3]))
				part.setChild("type", arr[1])
				partNum = partNum + 1
		return
