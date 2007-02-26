"""linux.unknown.restore.adjust.FSTab Module"""



import os
import volumeid

import cairn
from cairn.sysdefs.linux import Constants
import cairn.sysdefs.templates.unix.system.partitions.FSTab as FSTAB



def getClass():
	return FSTab()


class FSTab(object):

	def open(self, sysdef):
		fstabFile = os.path.join(sysdef.info.get("env/mountdir"), "etc/fstab")
		destName = cairn.backupFileDir(fstabFile)
		try:
			src = file(destName, "r")
			dest = file(fstabFile, "w")
			return src, dest
		except Exception, err:
			raise cairn.Exception("Failed to open %s: %s" % (fstabFile, err))
		return


	def probeVolID(self, device):
		try:
			(vusage, vtype, vver, vuuid,
			 vlabel, vlabel_safe) = volumeid.probe(device)
			return vuuid
		except Exception, err:
			raise cairn.Exception("Failed to id volume: %s" % cairn.strErr(err))
		return


	def filterFile(self, sysdef, src, dest, uuidParts, mdevParts):
		for line in src.readlines():
			wline = line
			if Constants.FSTAB_UUID_RE.search(line):
				arr = line.split()
				word = arr[FSTAB.DEVICE].lstrip("UUID=")
				for part in uuidParts:
					if part.get("fs/uuid") == word:
						newID = self.probeVolID(part.get("mapped-device"))
						cairn.verbose("Mapping %s -> %s on line:" %
									  (word, newID))
						cairn.verbose(line)
						dest.write("## " + line)
						wline = line.replace(word, newID)
						break
			elif FSTAB.FSTAB_LINE_RE.search(line):
				arr = line.split()
				dev = arr[FSTAB.DEVICE]
				for part in mdevParts:
					orgDev = part.get("device")
					if orgDev == dev:
						mappedDev = part.get("mapped-device")
						cairn.verbose("Mapping %s -> %s on line:" %
									  (orgDev, mappedDev))
						cairn.verbose(line)
						dest.write("## " + line)
						wline = line.replace(dev, mappedDev)
						break
			dest.write(wline)
		return


	def run(self, sysdef):
		uuidParts = []
		mdevParts = []
		for device in sysdef.readInfo.getElems("hardware/device"):
			for part in device.getElems("disk-label/partition"):
				if part.get("fs/mount-source") == "fs/uuid":
					uuidParts.append(part)
				elif part.get("device") != part.get("mapped-device"):
					mdevParts.append(part)
		if len(uuidParts) or len(mdevParts):
			if len(uuidParts):
				cairn.display("Fixing UUIDs in /etc/fstab")
			if len(mdevParts):
				cairn.display("Fixing mapped devices in /etc/fstab")
			(src, dest) = self.open(sysdef)
			self.filterFile(sysdef, src, dest, uuidParts, mdevParts)
		return True
