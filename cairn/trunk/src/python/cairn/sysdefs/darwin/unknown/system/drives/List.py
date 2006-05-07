"""darwin.unknown.hardware.Drives Module"""


import os
import commands
import re

import cairn
import cairn.sysdefs.templates.unix.hardware.Drives as tmpl


def getClass():
	return Drives()


class Drives(tmpl.Drives):
	def run(self, sysdef):
		drives = self.listDrives(sysdef)
		self.defineDrives(sysdef, drives)
		return True


	def listDrives(self, sysdef):
		ret = commands.getstatusoutput("%s -l" % sysdef.info.get("env/tools/disktool"))
		if ret[0] != 0:
			msg = "Failed to run %s to find drive information:\n" % sysdef.info.get("env/tools/disktool")
			raise cairn.Exception(msg + ret[1])
		drives = []
		for line in ret[1].split("\n"):
			arr = line.split("'")
			if len(arr) >= 3 and arr[0].find("Disk Appeared"):
				device = re.sub("s[0-9]*$", "", arr[1])
				if device not in drives:
					drives.append(device)
		return drives


	def defineDrives(self, sysdef, drives):
		for driveName in drives:
			ret = commands.getstatusoutput("%s info %s" % (sysdef.info.get("env/tools/diskutil"), driveName))
			if ret[0] != 0:
				msg = "Failed to run %s to find drive information:\n" % sysdef.info.get("env/tools/diskutil")
				raise cairn.Exception(msg + ret[1])
			if not re.search("Protocol:(\s)*Disk Image", ret[1]):
				drive = sysdef.info.createDriveElem(driveName)
				drive.setChild("device", "/dev/" + driveName)
		return
