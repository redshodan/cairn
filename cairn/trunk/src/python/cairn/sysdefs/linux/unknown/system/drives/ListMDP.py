"""linux.unknown.system.drives.ListMDP Module"""



import cairn
from cairn import Options
from cairn.sysdefs.linux import Shared



def getClass():
	return ListMDP()


class ListMDP(object):

	def run(self, sysdef):
		if Options.get("no-raid") or not sysdef.info.get("env/tools/lvm"):
			cairn.log("Skipping Software RAID check")
			return True
		cairn.log("Checking for Partitionable Software RAIDs")
		for devShort in Shared.listDevices():
			dtype = Shared.getDeviceType(devShort)
			if (dtype != "mdp"):
				continue
			cairn.displayRaw("  %s" % devShort)
			Shared.defineDevice(sysdef, devShort, dtype)
			cairn.displayNL()
		return True
