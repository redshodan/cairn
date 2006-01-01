"""linux.unknown.hardware.Drives.Drives2_6 Module"""


import os
import commands
import re

import cairn
import cairn.sysdefs.templates.unix.hardware.Drives as tmpl
from cairn.sysdefs.linux.unknown.hardware import Drives



def getClass():
	return Drives2_6()


class Drives2_6(tmpl.Drives):
	def run(self, sysdef):
		for device in os.listdir("/sys/block"):
			if not Drives.matchDevice(device):
				continue
			removable = file("/sys/block/%s/removable" % device, "r")
			for line in removable:
				break
			removable.close()
			if line.startswith("0"):
				drive = sysdef.info.createDriveElem(device)
				sysdef.info.setChild(drive, "device", "/dev/" + device)
		return True
