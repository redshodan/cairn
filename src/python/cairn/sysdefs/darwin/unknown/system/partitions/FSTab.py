"""templates.darwin.unknown.system.partitions.FSTab Module"""


# Mac OS/X doesnt have a fstab file...


import cairn.sysdefs.templates.unix.system.partitions.FSTab as impl


def getClass():
	return FSTab()


class FSTab(impl.FSTab):
	def run(self, sysdef):
		return True
