"""linux.unknown.system.lvm.List Module"""


import re

import pylibparted as parted

import cairn
from cairn import Options
from cairn.sysdefs.linux import Shared



def getClass():
	return List()


class List(object):

	def scanPVs(self, sysdef):
		cmd = "%s -u " % sysdef.info.get("env/tools/pvscan")
		output = cairn.run(cmd, "Failed to scan Physical Volumes")
		pvs = []
		pvsElem = sysdef.info.getElem("hardware/lvm-cfg/pvs")
		for line in output.split("\n"):
			line = line.strip()
			if re.match("^PV /dev/*", line):
				words = line.split()
				pvs.append(words[1])
				elem = pvsElem.createElem("pv", words[1], True)
				elem.setAttr("vg", words[6])
				elem.setAttr("uuid", words[4])
		if len(pvs):
			word = " ".join(pvs)
		else:
			word = "none"
		cairn.info("  PVs:  %s" % word)
		return pvs


	def scanVGs(self, sysdef):
		cmd = sysdef.info.get("env/tools/vgscan")
		output = cairn.run(cmd, "Failed to scan Volume Groups")
		vgs = []
		vgsElem = sysdef.info.getElem("hardware/lvm-cfg/vgs")
		for line in output.split("\n"):
			line = line.strip()
			if re.match("Found volume group ", line):
				words = line.split("\"")
				vgs.append(words[1])
				vgsElem.createElem("vg", words[1], True)
		if len(vgs):
			word = " ".join(vgs)
		else:
			word = "none"
		cairn.info("  VGs:  %s" % word)
		return vgs


	def scanLVs(self, sysdef):
		cmd = sysdef.info.get("env/tools/lvscan")
		output = cairn.run(cmd, "Failed to scan Logical Volumes")
		lvs = []
		lvsElem = sysdef.info.getElem("hardware/lvm-cfg/lvs")
		for line in output.split("\n"):
			line = line.strip()
			if re.match("^\S*\s*'.*'\s*\[\S*\s*\S*\]", line):
				words = line.split()
				full = words[1].strip("'")
				full = full[5:]
				words = full.split("/")
				vg = words[0]
				lv = words[1]
				lvs.append(full)
				elem = lvsElem.createElem("lv", lv, True)
				elem.setAttr("vg", vg)
		if len(lvs):
			word = " ".join(lvs)
		else:
			word = "none"
		cairn.info("  LVs:  %s" % word)
		return lvs


	def defineDevices(self, sysdef):
		skips = sysdef.info.getSkipDevices()
		skipped = []
		lvs = sysdef.info.getElems("hardware/lvm-cfg/lvs/lv")
		for vg in sysdef.info.getElems("hardware/lvm-cfg/vgs/vg"):
			vgname = vg.getText()
			vgdev = "/dev/" + vgname
			devElem = sysdef.info.createDeviceElem(vgname)
			devElem.setChild("device", vgdev)
			devElem.setChild("mapped-device", vgdev)
			devElem.setChild("type", "lvm")
			if Shared.skipDevice(skips, vgname):
				skipped.append(vgname)
				devElem.setChild("status", "skipped")
				continue
			devElem.setChild("status", "probed")
			dlabel = sysdef.info.createDiskLabelElem(devElem)
			dlabel.setChild("type", "lvm")
			count = 1
			for lv in lvs:
				if lv.getAttr("vg") != vgname:
					continue
				fulldev = "/dev/mapper/%s-%s" % (vgname, lv.getText())
				partElem = sysdef.info.createPartitionElem(devElem,
														   "%d" % count)
				partElem.setChild("device", fulldev)
				partElem.setChild("mapped-device", fulldev)
				empty = True
				try:
					pdev = parted.PedDevice(fulldev)
					pdisk = pdev.diskNew()
					pparts = pdisk.getPartitions()
					Shared.definePartition(sysdef, partElem, pparts[0])
					empty = False
				except Exception, err:
					cairn.displayNL()
					cairn.error("%s" % err)
				if empty:
					partElem.setChild("status", "empty")
				partElem.setChild("type", "loop")
				count = count + 1
		return True


	def run(self, sysdef):
		if Options.get("no-lvm") or not sysdef.info.get("env/tools/lvm"):
			cairn.log("Skipping LVM check")
			return True
		cairn.log("Checking for LVM volumes")
		pvs = self.scanPVs(sysdef)
		vgs = self.scanVGs(sysdef)
		lvs = self.scanLVs(sysdef)
		self.defineDevices(sysdef)
		return True
