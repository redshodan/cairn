"""linux.unknown.restore.resolve.MatchDrives Module"""


import cairn
import cairn.sysdefs.templates.unix.restore.resolve.MatchDrives as tmpl


#
# Very simple straight up matching of drive devices. Put something more complex
# in later
#


def getClass():
	return MatchDrives()


class MatchDrives(tmpl.MatchDrives):

	def match(self, sysdef):
		sysDrives = sysdef.info.getElems("hardware/drive")
		imgDrives = sysdef.readInfo.getElems("hardware/drive")
		for index in range(len(sysDrives)):
			sysDev = sysDrives[index].get("device")
			imgDev = imgDrives[index].get("device")
			cairn.verbose("Mapping image drive %s to system drive %s" % (imgDev, sysDev))
			imgDrives[index].setChild("mapped-device", sysDev)
			for part in imgDrives[index].getElems("partition"):
				dev = part.get("device")
				mapped = dev.replace(imgDev, sysDev)
				cairn.verbose("Mapping partition device: %s -> %s" % (dev, mapped))
				part.setChild("mapped-device", mapped)
		return


	def check(self, sysdef):
		perfect = True
		devs = True
		partial = False
		sysDrives = sysdef.info.getElems("hardware/drive")
		imgDrives = sysdef.readInfo.getElems("hardware/drive")
		for index in range(len(sysDrives)):
			if sysDrives[index].get("device") == imgDrives[index].get("device"):
				partial = True
				if not ((sysDrives[index].get("model") ==
						 imgDrives[index].get("model")) and
						(sysDrives[index].get("size") ==
						 imgDrives[index].get("size"))):
					perfect = False
			else:
				devs = False
		if perfect:
			sysdef.readInfo.setChild("hardware/drive-match", "perfect")
			return True
		elif devs:
			sysdef.readInfo.setChild("hardware/drive-match", "devices")
			return True
		elif partial:
			sysdef.readInfo.setChild("hardware/drive-match", "partial")
			return False
		else:
			sysdef.readInfo.setChild("hardware/drive-match", "none")
			return False


	def run(self, sysdef):
		if not self.check(sysdef):
			raise cairn.Exception("Failed to match image drives to system drives. The next version of CAIRN will be much more inteligent about this and will be able to dynamically adjust the image to fit the system.")
		self.match(sysdef)
		return True
