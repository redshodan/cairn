"""linux.unknown.system.drives.ListMD Module"""



import cairn
from cairn import Options
from cairn.sysdefs.linux import Shared



def getClass():
	return ListMD()


class ListMD(object):

	# TODO: do skips

	def run(self, sysdef):
		if Options.get("no-raid") or not sysdef.info.get("env/tools/lvm"):
			cairn.log("Skipping Software RAID check")
			return True
		cairn.log("Checking for Software RAIDs")
		for devShort in Shared.listDevices():
			dtype = Shared.getDeviceType(devShort)
			if (dtype != "md"):
				continue
			cairn.displayRaw("  %s" % devShort)
			Shared.defineDevice(sysdef, devShort, dtype)
			cairn.displayNL()
		return True
