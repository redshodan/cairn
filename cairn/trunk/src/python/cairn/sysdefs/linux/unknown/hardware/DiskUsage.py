"""templates.unix.hardware.DiskUsage Module"""


import os
import commands
import re

import cairn
import cairn.sysdefs.templates.unix.hardware.DiskUsage as tmpl



def getClass():
	return DiskUsage()



class DiskUsage(tmpl.DiskUsage):
	def run(self, sysdef):
		for drive in sysdef.info.getElems("hardware/drive"):
			for partition in sysdef.info.getElems("partition", drive):
				self.findPartitionDiskUsage(sysdef, partition)
		return True


	def findPartitionDiskUsage(self, sysdef, partition):
		if (not sysdef.info.get("mount", partition) or
			(sysdef.info.get("mount", partition) == "none")):
			return
		cmd = "%s -k %s" % (sysdef.info.get("env/diskfree"),
							sysdef.info.get("mount", partition))
		ret = commands.getstatusoutput(cmd)
		if ret[0] != 0:
			msg = "Failed to run %s to find disk usage information:\n" % sysdef.info.get("env/diskfree")
			raise cairn.Exception(msg + ret[1])
		device = sysdef.info.get("device", partition)
		space = None
		for line in ret[1].split("\n"):
			if line.startswith(device):
				arr = line.split()
				space = sysdef.info.createPartitionSpaceElem(partition)
				sysdef.info.setChild(space, "total", arr[1])
				sysdef.info.setChild(space, "used", arr[2])
				sysdef.info.setChild(space, "free", arr[3])
				break
		if not space:
			raise cairn.Exception("'df' returned a different device for mount '%s'. Perhaps this not mounted." % sysdef.info.get("mount", partition))
		return
