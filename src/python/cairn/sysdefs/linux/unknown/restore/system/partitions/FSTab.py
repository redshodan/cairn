"""linux.unknown.restore.system.partitions.FSTab Module"""



import cairn.sysdefs.templates.unix.system.partitions.FSTab as tmpl


#
# We dont care about the boot environments fstab during restore
#


def getClass():
	return FSTab()


class FSTab(tmpl.FSTab):

	def run(self, sysdef):
		return True
