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
			if sysdef.info.skipDevice(devShort):
				skipped.append(devShort)
				devElem.setChild("status", "skipped")
				continue
			devElem.setChild("status", "probed")
			dlabel = sysdef.info.createDiskLabelElem(devElem)
			dlabel.setChild("type", dtype)
			self.defineMDConfig(sysdef, devElem, devFull)
			
			try:
				pdev = parted.PedDevice(devFull)
				pdisk = pdev.diskNew()
				ptype = pdisk.getType()
				dlabel.setChild("type", ptype.getName())
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
				cairn.error("Failed to probe partition table: %s" % err)
		cairn.displayNL()
		if len(skipped):
			cairn.display("Skipped Software RAIDs: %s" % " ".join(skipped))
		return


	def defineMDConfig(self, sysdef, devElem, devFull):
		mdcfg = sysdef.info.createDeviceMDConfigElem(devElem)
		mdcfg.setChild("md-dev", devFull)
		cmd = "%s -D %s" % (sysdef.info.get("env/tools/mdadm"), devFull)
		output = cairn.run(cmd, "Failed to scan Software Raid %s" % devFull)
		for line in output.split("\n"):
			line = line.strip()
			if line.find("Raid Level :") >= 0:
				words = line.split(":")
				mdcfg.setChild("level", words[1].strip())
			if line.find("Layout :") >= 0:
				words = line.split(":")
				mdcfg.setChild("layout", words[1].strip())
			if line.find("Chunk Size :") >= 0:
				words = line.split(":")
				mdcfg.setChild("chunk", words[1].strip().rstrip("K"))
			if line.find("active") >= 0:
				words = line.split()
				sysdef.info.createDeviceMDDeviceElem(mdcfg, words[-1], "active")
			if line.find("spare") >= 0:
				words = line.split()
				sysdef.info.createDeviceMDDeviceElem(mdcfg, words[-1], "spare")
		return mdcfg


	def run(self, sysdef):
		if Options.get("no-raid") or not sysdef.info.get("env/tools/md"):
			cairn.info("Skipping Software RAID check")
			return True
		cairn.log("Checking for Software RAIDs")
		mds = self.listDevices(sysdef)
		self.defineDevices(sysdef, mds)
		return True
