"""linux.unknown.restore.setup.CreateLogical.CreateMD Module"""


def getClass():
	return CreateMD()


class CreateMD(object):

	def createMD(self, sysdef, device):
		dev = device.get("device")
		type = device.get("type")
		rlevel = device.get("md-cfg/level").replace("raid", "")
		chunk = device.get("md-cfg/chunk")
		if type == "md":
			auto = "-ayes"
		else:
			auto = "-ap63"
		rdevs = []
		rspares = []
		for rdevice in device.getElems("md-cfg/device"):
			if rdevice.getAttr("state") == "active":
				rdevs.append(rdevice.getText())
			elif rdevice.getAttr("state") == "spare":
				rdevs.append(rspares.getText())
		cmd = "%s --create %s --level %s --chunk %s --raid-devices=%d %s" + \
			  " --spare-devices=%d %s" % \
			  (sysdef.info.get("env/tools/mdadm"),
			   dev, auto, rlevel, chunk, len(rdevs), " ".join(rdevs),
			   len(rspares), " ".join(rspares))
		cairn.run(cmd, "Failed to create Software RAID %s" % dev)
		return


	def run(self, sysdef):
		cairn.log("Recreating Software RAIDs:")
		for device in sysdef.readInfo.getElems("hardware/device"):
			if ((device.get("status") == "probed") and
				((device.get("type") == "md") or
				 (device.get("type") == "mdp"))):
				cairn.displayRaw("  %s" % device.get("device"))
				self.createMD(sysdef, device)
		cairn.displayNL()
		return True
