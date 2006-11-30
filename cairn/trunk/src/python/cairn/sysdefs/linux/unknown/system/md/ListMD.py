"""linux.unknown.system.md.ListMD Module"""


###
### This should be broken up some. Also maybe generic sub-devices in the meta.
###



import re
import pylibparted as parted

import cairn
from cairn import Logging
from cairn import Options
from cairn.sysdefs.linux import Shared



def getClass():
	return ListMD()


class ListMD(object):

	def listDevices(self, sysdef):
		cmd = "%s -Ds" % sysdef.info.get("env/tools/mdadm")
		output = cairn.run(cmd, "Failed to scan Software Raids")
		mds = {}
		for line in output.split("\n"):
			line = line.strip()
			if re.match("^ARRAY*", line):
				words = line.split()
				mds[words[1]] = words[2:]
		cairn.verbose("Found: %s" % " ".join(mds.keys()))
		return mds


	def defineDevices(self, sysdef, mds):
		skips = sysdef.info.getSkipDevices()
		skipped = []
		fullDevs = mds.keys()
		fullDevs.sort()
		for devFull in fullDevs:
			devShort = devFull.strip("/dev/")
			cairn.displayRaw("  %s" % devShort)
			dtype = Shared.getDeviceType(devShort)
			devElem = sysdef.info.createDeviceElem(devShort)
			devElem.setChild("device", devFull)
			devElem.setChild("mapped-device", devFull)
			devElem.setChild("type", dtype)
			if Shared.skipDevice(skips, devShort):
				skipped.append(devShort)
				devElem.setChild("status", "skipped")
				continue
			devElem.setChild("status", "probed")
			dlabel = sysdef.info.createDiskLabelElem(devElem)
			dlabel.setChild("type", dtype)

			try:
				pdev = parted.PedDevice(devFull)
				pdisk = pdev.diskNew()
				pparts = pdisk.getPartitions()
				count = 1
				for ppart in pparts:
					partElem = sysdef.info.createPartitionElem(devElem,
															   "%d" % count)
					if dtype == "md":
						partElem.setChild("device", devFull)
					else:
						partElem.setChild("device", ppart.getPath())
					partElem.setChild("mapped-device", partElem.get("device"))
					empty = True
					try:
						Shared.definePartition(sysdef, partElem, ppart)
						empty = False
					except Exception, err:
						cairn.displayNL()
						Logging.error.log(Logging.ERROR, str(err))
					if empty:
						partElem.setChild("status", "empty")
					if dtype == "md":
						partElem.setChild("type", "loop")
					count = count + 1
			except Exception, err:
				cairn.displayNL()
				raise cairn.Exception("Failed to probe partition table", err)
		cairn.displayNL()
		if len(skipped):
			cairn.display("Skipped Software RAIDs: %s" % " ".join(skipped))
		return


	def run(self, sysdef):
		if Options.get("no-raid") or not sysdef.info.get("env/tools/lvm"):
			cairn.log("Skipping Software RAID check")
			return True
		cairn.log("Checking for Software RAIDs")
		mds = self.listDevices(sysdef)
		self.defineDevices(sysdef, mds)
		return True
