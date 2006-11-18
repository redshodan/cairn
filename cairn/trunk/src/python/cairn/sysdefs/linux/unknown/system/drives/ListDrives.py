"""linux.unknown.system.drives.ListDrives Module"""



import cairn
from cairn.sysdefs.linux import Shared



def getClass():
	return ListDrives()


class ListDrives(object):

	def run(self, sysdef):
		cairn.log("Checking for drives")
		for devShort in Shared.listDevices():
			dtype = Shared.getDeviceType(devShort)
			if (dtype != "drive"):
				continue
			cairn.displayRaw("  %s" % devShort)
			Shared.defineDevice(sysdef, "/dev/" + devShort, devShort, dtype)
		cairn.displayNL()
		return True
