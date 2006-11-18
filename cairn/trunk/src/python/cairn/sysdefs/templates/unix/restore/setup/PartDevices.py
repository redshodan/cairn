"""templates.unix.restore.setup.PartDevices Module"""


import cairn



def getClass():
	return PartDevices()


class PartDevices(object):

	def partitionDevice(self, sysdef, device):
		return


	def run(self, sysdef):
		cairn.log("Partitioning devices:")
		for device in sysdef.readInfo.getElems("hardware/device"):
			if not device.get("empty"):
				cairn.displayRaw("  %s" % device.get("device"))
				self.partitionDevice(sysdef, device)
		return True
