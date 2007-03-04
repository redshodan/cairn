"""linux.unknown.restore.setup.CreateLogical.CreateMD Module"""


import os

import cairn
from cairn.sysdefs.linux.unknown.restore.setup import PartDevicesParted


def getClass():
	return CreateMD()


class CreateMD(object):

	def zeroDev(self, sysdef, dev):
		cmd = "%s --zero-superblock --force %s" % \
			  (sysdef.info.get("env/tools/mdadm"), dev)
		cairn.run(cmd, "Failed to zero device %s" % dev)
		return


	def createMD(self, sysdef, device, devmap):
		dev = device.get("device")
		type = device.get("type")
		rlevel = device.get("md-cfg/level").replace("raid", "")
		chunk = ""
		if device.get("md-cfg/chunk"):
			chunk = "--chunk %s" % device.get("md-cfg/chunk")
		if type == "md":
			auto = "-ayes"
		else:
			auto = "-ap63"
		rdevs = []
		rspares = []
		for rdevice in device.getElems("md-cfg/device"):
			mapped = sysdef.readInfo.mapDevice(devmap, rdevice.getText())
			self.zeroDev(sysdef, mapped)
			if rdevice.getAttr("state") == "active":
				rdevs.append(mapped)
			elif rdevice.getAttr("state") == "spare":
				rspares.append(mapped)
		cmd = "yes | %s --create %s %s --level %s %s --raid-devices=%d %s" % \
			  (sysdef.info.get("env/tools/mdadm"),
			   dev, auto, rlevel, chunk, len(rdevs), " ".join(rdevs))
		if len(rspares):
			cmd = "%s --spare-devices=%d %s" % (cmd, len(rspares),
												" ".join(rspares))
		cairn.run(cmd, "Failed to create Software RAID %s" % dev)
		if type == "mdp":
			self.partitionMD(sysdef, device)
		return


	def partitionMD(self, sysdef, device):
		parter = PartDevicesParted.PartDevicesParted()
		parter.partitionDevice(sysdef, device)
		return


	def run(self, sysdef):
		cairn.log("Recreating Software RAIDs:")
		devmap = sysdef.readInfo.getDeviceMap()
		for device in sysdef.readInfo.getElems("hardware/device"):
			if ((device.get("status") == "probed") and
				((device.get("type") == "md") or
				 (device.get("type") == "mdp"))):
				cairn.displayRaw("  %s" % device.get("device"))
				self.createMD(sysdef, device, devmap)
		cairn.displayNL()
		return True
