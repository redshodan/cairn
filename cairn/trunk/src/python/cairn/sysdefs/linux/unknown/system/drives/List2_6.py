"""linux.unknown.system.drives.List2_6 Module"""


import os
import re
import commands

import cairn
import cairn.sysdefs.templates.unix.system.drives.List as tmpl
from cairn.sysdefs.linux import Shared



def getClass():
	return List2_6()


class List2_6(tmpl.List):

	def run(self, sysdef):
		cairn.log("Checking drives")
		for device in os.listdir("/sys/block"):
			if not Shared.matchDevice(device):
				continue
			removable = file("/sys/block/%s/removable" % device, "r")
			for line in removable:
				break
			removable.close()
			if line.startswith("0"):
				drive = sysdef.info.createDriveElem(device)
				drive.setChild("device", "/dev/" + device)
				cmd = "%s -s %s" % (sysdef.info.get("env/tools/part"),
									drive.get("device"))
				ret = commands.getstatusoutput(cmd)
				if ret[0] != 0:
					msg = "Failed to run %s to find drive size:\n" % sysdef.info.get("env/tools/part")
					raise cairn.Exception(msg + ret[1])
				drive.setChild("size", ret[1].strip())
		return True
