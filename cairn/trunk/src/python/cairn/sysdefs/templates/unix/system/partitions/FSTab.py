"""templates.unix.system.partitions.FSTab Module"""


import os
import re

import cairn


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
		devices = sysdef.info.getElems("hardware/device")
		for device in devices:
			partitions = partitions + device.getElems("disk-label/partition")
		try:
			fstab = file(self.fstabFile(), "rb")
		except Exception, err:
			raise cairn.Exception("Failed to open %s: %s" %
								  (self.fstabFile(), err))
		for line in fstab:
			if (not re.search("^\s*\#", line) and
				re.search("\s*[/_\-a-zA-Z0-9]+\s+[/a-zA-Z0-9]+\s+[a-zA-Z0-9]+\s+[=,\-a-zA-Z0-9]+\s+[0-9]+\s+[0-9]+", line)):
				arr = line.split()
				for part in partitions:
					if part.get("device") == arr[DEVICE]:
						#part.setChild("fs-type", arr[FS])
						part.setChild("mount", arr[MNT])
		return True
