"""linux.unknown.restore.setup.MatchDrives Module"""


import cairn
import cairn.sysdefs.templates.unix.restore.setup.MatchDrives as tmpl


#
# Very simple straight up matching of drive devices. Put something more complex
# in later
#


def getClass():
	return MatchDrives()


class MatchDrives(tmpl.MatchDrives):

	def run(self, sysdef):
		sysDrives = sysdef.info.getElems("hardware/drive")
		imgDrives = sysdef.readInfo.getElems("hardware/drive")
		for index in range(len(sysDrives)):
			sysDev = sysDrives[index].get("device")
			imgDev = imgDrives[index].get("device")
			cairn.log("Mapping image drive %s to real drive %s" % (imgDev, sysDev))
			imgDrives[index].setChild("mapped-device", sysDev)
			for part in imgDrives[index].getElems("partition"):
				dev = part.get("device")
				mapped = dev.replace(imgDev, sysDev)
				cairn.verbose("Mapping partition device: %s -> %s" % (dev, mapped))
				part.setChild("mapped-device", mapped)
		return True
