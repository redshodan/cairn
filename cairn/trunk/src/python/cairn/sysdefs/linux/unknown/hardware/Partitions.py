"""linux.unknown.hardware.Partitions Module"""


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
		cmd = "%s -l %s" % (sysdef.info.get("env/tools/part"),
							sysdef.info.get("device", drive))
		ret = commands.getstatusoutput(cmd)
		if ret[0] != 0:
			msg = "Failed to run %s to find drive information:\n" % sysdef.info.get("env/tools/part")
			raise cairn.Exception(msg + ret[1])
		sysdef.info.setChild(drive, "part-tool-cfg", ret[1])
		partNum = 1
		for line in ret[1].split("\n"):
			if line.startswith("/dev/"):
				if line.endswith("Empty"):
					partNum = partNum + 1
					continue
				arr = line.split()
				offset = 0
				if arr[1] == "*":
					offset = 1
				part = sysdef.info.createPartitionElem(drive, "%d" % partNum)
				sysdef.info.setChild(part, "device", arr[0])
				sysdef.info.setChild(part, "type", arr[5 + offset])
				partNum = partNum + 1
		return
