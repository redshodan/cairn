"""templates.unix.system.partitions.DiskUsage Module"""



import sys
import re

import cairn


def getClass():
	return DiskUsage()



class DiskUsage(object):

	def mount(self, partition):
		raise cairn.Exception("Unimplimented function: mount")


	def askMount(self, sysdef, partition):
		mount = partition.get("mount")
		cairn.displayRaw("Mount %s is not mounted. Do you wish to have it mounted now so its included in the backup? [Y/n]" % mount)
		line = sys.stdin.readline()
		line = line.strip()
		cairn.displayNL()
		if not line or (len(line) == 0) or re.match("[yY]", line):
			self.mount(sysdef, partition)
			return True
		else:
			cairn.display("Skipping mount point %s", partition.get("mount"))
			return False


	def run(self, sysdef):
		return True
