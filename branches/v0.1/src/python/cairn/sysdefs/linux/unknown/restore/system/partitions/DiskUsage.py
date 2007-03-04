"""linux.unknown.restore.system.partitions.DiskUsage Module"""


import cairn.sysdefs.linux.unknown.system.partitions.DiskUsage as tmpl


#
# We dont care about the boot environments disk usage during restore
#


def getClass():
	return DiskUsage()



class DiskUsage(tmpl.DiskUsage):
	def run(self, sysdef):
		return True
