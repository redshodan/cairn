"""templates.unix.system.partitions.FSTab Module"""


import os
import re


DEVICE = 0
MNT = 1
FS = 2
OPTS = 3


def getClass():
	return FSTab()


class FSTab(object):


	def fstabFile(self):
		return "/etc/fstab"


	def run(self, sysdef):
		partitions = []
		drives = sysdef.info.getElems("hardware/drive")
		for drive in drives:
			partitions = partitions + sysdef.info.getElems("partition", drive)
		fstab = file(self.fstabFile(), "rb")
		for line in fstab:
			if (not re.search("^\s*\#", line) and
				re.search("\s*[/a-zA-Z0-9]+\s+[/a-zA-Z0-9]+\s+[a-zA-Z0-9]+\s+[,\-a-zA-Z0-9]+\s+[0-9]+\s+[0-9]+", line)):
				arr = line.split()
				for part in partitions:
					if sysdef.info.get("device", part) == arr[DEVICE]:
						sysdef.info.setChild(part, "fs-type", arr[FS])
						sysdef.info.setChild(part, "mount", arr[MNT])
		return True
