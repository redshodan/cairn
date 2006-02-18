"""templates.unix.hardware.DiskUsage Module"""


import os
from statvfs import *

import cairn
import cairn.sysdefs.templates.unix.hardware.DiskUsage as tmpl



def getClass():
	return DiskUsage()



class DiskUsage(tmpl.DiskUsage):
	def run(self, sysdef):
		cairn.verbose("Sizing partitions")
		for drive in sysdef.info.getElems("hardware/drive"):
			for partition in sysdef.info.getElems("partition", drive):
				self.findPartitionDiskUsage(sysdef, partition)
		return True


	def findPartitionDiskUsage(self, sysdef, partition):
		if (not sysdef.info.get("mount", partition) or
			(sysdef.info.get("mount", partition) == "none")):
			return
		info = os.statvfs(sysdef.info.get("mount", partition))
		total = "%d" % ((info[F_BLOCKS] * 4) / 1024)
		used = "%d" % (((info[F_BLOCKS] - info[F_BAVAIL]) * 4) / 1024)
		free = "%d" % ((info[F_BAVAIL] * 4) / 1024)
		device = sysdef.info.get("device", partition)
		space = sysdef.info.createPartitionSpaceElem(partition)
		sysdef.info.setChild(space, "total", total)
		sysdef.info.setChild(space, "used", used)
		sysdef.info.setChild(space, "free", free)
		cairn.verbose("  %s: space: total=%sM used=%sM free=%sM" % \
					  (device, total, used, free))
		return
