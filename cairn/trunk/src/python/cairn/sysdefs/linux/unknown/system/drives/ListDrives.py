"""linux.unknown.system.drives.ListDrives Module"""



import cairn
from cairn.sysdefs.linux import Shared



def getClass():
	return ListDrives()


class ListDrives(object):

	def run(self, sysdef):
		cairn.log("Checking for drives")
		skips = sysdef.info.getSkipDevices("drive")
		skipped = []
		found = False
		for devShort in Shared.listDevices():
			dtype = Shared.getDeviceType(devShort)
			if (dtype != "drive"):
				continue
			if Shared.skipDevice(skips, devShort):
				skipped.append(devShort)
				Shared.defineDeviceSkipped(sysdef, "/dev/" + devShort, devShort,
										   dtype)
			else:
				found = True
				cairn.displayRaw("  %s" % devShort)
				Shared.defineDevice(sysdef, "/dev/" + devShort, devShort, dtype)
		cairn.displayNL()
		if len(skipped):
			cairn.display("Skipped drives: %s" % " ".join(skipped))
		if not found:
			raise cairn.Exception("No drives found or all drives were skipped.")
		return True
