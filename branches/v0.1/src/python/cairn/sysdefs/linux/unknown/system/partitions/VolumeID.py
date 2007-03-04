"""linux.unknown.system.partitions.VolumeID Module"""


import volumeid

import cairn
from cairn.sysdefs.linux import Shared



def getClass():
	return VolumeID()



class VolumeID(object):

	def run(self, sysdef):
		cairn.log("Checking filesystems")
		for device in sysdef.info.getElems("hardware/device"):
			if device.get("status") != "probed":
				continue
			for part in device.getElems("disk-label/partition"):
				dev = part.get("device")
				cairn.displayRaw("  %s: " % dev.lstrip("/dev/"))
				try:
					(vusage, vtype, vver, vuuid,
					 vlabel, vlabel_safe) = volumeid.probe(dev)
					part.setChild("fs/type", vtype)
					if ((vusage == "filesystem") or
						((vusage == "other") and (vtype == "swap"))):
						part.setChild("fs/is-normal", "True")
					if (vver):
						part.setChild("fs/version", vver)
					if (vuuid):
						part.setChild("fs/uuid", vuuid)
					if (vlabel):
						part.setChild("fs/label", vlabel)
					if (vlabel_safe):
						part.setChild("fs/label_safe", vlabel_safe)
					cairn.display("%s %s" % (vusage, vtype.rstrip("_member")))
				except Exception, err:
					cairn.display("Unknown")
					cairn.verbose("Failed to id volume: %s" % cairn.strErr(err))
		return True
