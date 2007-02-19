"""linux.unknown.system.partitions.DiskUsage Module"""


import os
import os.path
from statvfs import *

import cairn
import cairn.sysdefs.templates.unix.system.partitions.DiskUsage as tmpl
from cairn.sysdefs.linux import Shared



def getClass():
	return DiskUsage()



class DiskUsage(tmpl.DiskUsage):

	def mount(self, sysdef, partition):
		Shared.mount(sysdef, partition.get("device"), partition.get("fs/mount"))
		return


	def findPartitionDiskUsage(self, sysdef, partition):
		mount = partition.get("fs/mount")
		if not mount or (mount == "none"):
			return
		if not os.path.ismount(mount):
			if not self.askMount(sysdef, partition):
				return
		info = os.statvfs(mount)
		total = "%d" % ((info[F_BLOCKS] * 4) / 1024)
		used = "%d" % (((info[F_BLOCKS] - info[F_BAVAIL]) * 4) / 1024)
		free = "%d" % ((info[F_BAVAIL] * 4) / 1024)
		device = partition.get("device")
		fs = partition.getElem("fs")
		fs.setChild("total", total)
		fs.setChild("used", used)
		fs.setChild("free", free)
		cairn.verbose("  %s: space: total=%sM used=%sM free=%sM" % \
					  (device, total, used, free))
		return


	def run(self, sysdef):
		cairn.verbose("Sizing partitions")
		for device in sysdef.info.getElems("hardware/device"):
			for partition in device.getElems("disk-label/partition"):
				self.findPartitionDiskUsage(sysdef, partition)
		return True
