"""templates.unix.system.partitions.FSTab Module"""


import os
import re

import cairn


DEVICE = 0
MNT = 1
FS = 2
OPTS = 3
FSTAB_LINE_RE = re.compile("\s*/[^\s]+\s+/[^\s]*\s+[a-zA-Z0-9]+\s+[=,\-a-zA-Z0-9]+\s+[0-9]+\s+[0-9]+")



def getClass():
	return FSTab()


class FSTab(object):


	def fstabFile(self):
		return "/etc/fstab"


	def matchComment(self, line):
		if re.search("^\s*\#", line):
			return True
		else:
			return False


	def match(self, line):
		if FSTAB_LINE_RE.search(line):
			arr = line.split()
			return ("device", arr[DEVICE])
		else:
			return (None, None)


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
			if self.matchComment(line):
				continue
			(elemName, word) = self.match(line)
			if elemName and word:
				arr = line.split()
				for part in partitions:
					if part.get(elemName) == word:
						part.setChild("fs/mount", arr[MNT])
						part.setChild("fs/mount-source", elemName)
		return True
