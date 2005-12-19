"""templates.unix.hardware.Drives Module"""


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
		ret = commands.getstatusoutput("%s -l" % sysdef.info.get("env/disktool"))
		if ret[0] != 0:
			msg = "Failed to run %s to find drive information:\n" % sysdef.info.get("env/disktool")
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
			ret = commands.getstatusoutput("%s info %s" % (sysdef.info.get("env/diskutil"), driveName))
			if ret[0] != 0:
				msg = "Failed to run %s to find drive information:\n" % sysdef.info.get("env/diskutil")
				raise cairn.Exception(msg + ret[1])
			if not re.search("Protocol:(\s)*Disk Image", ret[1]):
				drive = sysdef.info.createDriveElem(driveName)
				sysdef.info.setChild(drive, "device", "/dev/" + driveName)
				self.definePartitions(sysdef, drive)
		return


	def definePartitions(self, sysdef, drive):
		ret = commands.getstatusoutput("%s list %s" % (sysdef.info.get("env/diskutil"), drive.getAttribute("name")))
		if ret[0] != 0:
			msg = "Failed to run %s to find drive information:\n" % sysdef.info.get("env/diskutil")
			raise cairn.Exception(msg + ret[1])
		partNum = 1
		for line in ret[1].split("\n"):
			arr = line.split()
			if (arr[0] != "0:") and re.match("[0-9]*:", arr[0]):
				part = sysdef.info.createPartitionElem(drive, "%d" % partNum)
				sysdef.info.setChild(part, "device", "/dev/" + arr[len(arr) - 1])
				sysdef.info.setChild(part, "label", " ".join(arr[2:len(arr) - 3]))
				sysdef.info.setChild(part, "type", arr[1])
				partNum = partNum + 1
		return
