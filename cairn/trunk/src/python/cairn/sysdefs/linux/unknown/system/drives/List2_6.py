"""linux.unknown.system.drives.List2_6 Module"""


import os
import re

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
		return True
