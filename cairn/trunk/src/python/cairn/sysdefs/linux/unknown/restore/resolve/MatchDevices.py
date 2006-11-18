"""linux.unknown.restore.resolve.MatchDevices Module"""


import cairn
import cairn.sysdefs.templates.unix.restore.resolve.MatchDevices as tmpl


#
# Very simple straight up matching of devices. Put something more complex
# in later
#


def getClass():
	return MatchDevices()


class MatchDevices(tmpl.MatchDevices):

	def match(self, sysdef):
		sysDevices = sysdef.info.getElems("hardware/device")
		imgDevices = sysdef.readInfo.getElems("hardware/device")
		for index in range(len(sysDevices)):
			sysDev = sysDevices[index].get("device")
			imgDev = imgDevices[index].get("device")
			cairn.verbose("Mapping image device %s to system device %s" % (imgDev, sysDev))
			imgDevices[index].setChild("mapped-device", sysDev)
			for part in imgDevices[index].getElems("disk-label/partition"):
				dev = part.get("device")
				mapped = dev.replace(imgDev, sysDev)
				cairn.verbose("Mapping partition device: %s -> %s" % (dev, mapped))
				part.setChild("mapped-device", mapped)
		return


	def check(self, sysdef):
		perfect = True
		devs = True
		partial = False
		sysDevices = sysdef.info.getElems("hardware/device")
		imgDevices = sysdef.readInfo.getElems("hardware/device")
		for index in range(len(sysDevices)):
			if sysDevices[index].get("device") == imgDevices[index].get("device"):
				partial = True
				if not ((sysDevices[index].get("model") ==
						 imgDevices[index].get("model")) and
						(sysDevices[index].get("sector-size") ==
						 imgDevices[index].get("sector-size")) and
						self.compareGeom(sysDevices[index].getElem("bios-geom"),
										 imgDevices[index].
										     getElem("bios-geom")) and
						self.compareGeom(sysDevices[index].getElem("hw-geom"),
										 imgDevices[index].
										     getElem("hw-geom")) and
						(sysDevices[index].get("type") ==
						 imgDevices[index].get("type")) and
						(sysDevices[index].get("size") ==
						 imgDevices[index].get("size"))):
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


	def compareGeom(self, sysGeom, imgGeom):
		if ((sysGeom.get("c") == imgGeom.get("c")) and
			(sysGeom.get("h") == imgGeom.get("h")) and
			(sysGeom.get("s") == imgGeom.get("s"))):
			return True
		else:
			return False


	def run(self, sysdef):
		if not self.check(sysdef):
			raise cairn.Exception("Failed to match image drives to system drives. The next version of CAIRN will be much more inteligent about dynamically adjust the image to fit the system.")
		self.match(sysdef)
		return True
