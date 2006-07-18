"""linux.unknown.system.drives.List2_6 Module"""


import os
import re
import commands

import cairn
from cairn.sysdefs.linux import Shared



def getClass():
	return List2_6()


class List2_6(object):

	def run(self, sysdef):
		cairn.log("Checking drives")
		list = os.listdir("/sys/block")
		list.sort()
		cairn.debug("All drives found: %s" % " ".join(list))
		for device in list:
			if not Shared.matchDevice(device):
				continue
			removable = file("/sys/block/%s/removable" % device, "r")
			for line in removable:
				break
			removable.close()
			if line.startswith("0"):
				cairn.displayRaw("  %s" % device)
				drive = sysdef.info.createDriveElem(device)
				drive.setChild("device", "/dev/" + device)
				cmd = "%s -s %s" % (sysdef.info.get("env/tools/part"),
									drive.get("device"))
				ret = commands.getstatusoutput(cmd)
				if ret[0] != 0:
					msg = "Failed to run %s to find drive size:\n" % sysdef.info.get("env/tools/part")
					raise cairn.Exception(msg + ret[1])
				drive.setChild("size", ret[1].strip())
				model = self.findModel(device)
				if model:
					drive.setChild("model", model)
		cairn.displayNL()
		return True


	def logSCSI(self):
		try: os.stat("/proc/scsi/scsi")
		except: return
		try:
			scsi = file("/proc/scsi/scsi")
			contents = scsi.read()
			cairn.debug("/proc/scsi/scsi\n%s" % contents)
		except Exception, err:
			cairn.verbose("Failed to read /proc/scsi/scsi: %s" %
						  cairn.strErr(err))
		return


	def findModel(self, device):
		try:
			if device[0] == "h":
				return self.findModelIDE(device)
			elif device[0] == "s":
				return self.findModelSCSI(device)
		except Exception, err:
			cairn.verbose("Failed to find model for %s: %s" %
						  (device, cairn.strErr(err)))
			return None


	def findModelIDE(self, device):
		modelFile = file("/proc/ide/%s/model" % device)
		for line in modelFile:
			break
		modelFile.close()
		return line.strip()


	def findModelSCSI(self, device):
		# cheesy and limited, yes I know
		letters = "abcdefghijklmnopqrstuvwxyz"
		scsi = file("/proc/scsi/scsi")
		contents = scsi.read()
		cairn.debug("/proc/scsi/scsi\n%s" % contents)
		dev = -1
		model = None
		type = None
		for line in scsi:
			if re.match("^Host:", line):
				dev = dev + 1
			if re.match("^\s*Vendor:", line):
				array = line.split(":")
				model = array[2].rstrip("Rev").strip()
			if re.match("^\s*Type:", line):
				array = line.split(":")
				type = array[1].rstrip("SCSI revision").rstrip("ANSI").strip()
			if (dev >= 0) and model and (type == "Direct-Access"):
				if device == "sd%s" % letters[dev]:
					scsi.close()
					return model
				model = None
				type = None
		scsi.close()
		return None
