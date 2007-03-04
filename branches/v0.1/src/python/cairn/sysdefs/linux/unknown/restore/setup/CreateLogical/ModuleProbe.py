"""linux.unknown.setup.PartDevicesParted Module"""


#
# It seems that the kernel doesn't like to autoprobe the software raid modules
# right now. So force it to happen before it becomes an issue. Do it here so
# restore will work better on any old linux distro.
#


import cairn
from cairn.sysdefs.linux import Constants



def getClass():
	return ModuleProbe()


class ModuleProbe(object):

	def run(self, sysdef):
		cairn.log("Probing Software RAID modules:")
		for module in Constants.KERNEL_MODULES:
			cairn.run("modprobe %s" % module,
					  "Failed to modprobe %s" % module)
		return True
