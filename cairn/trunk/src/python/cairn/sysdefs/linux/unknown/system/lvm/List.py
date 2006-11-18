"""linux.unknown.system.lvm.List Module"""


import re
import commands

import pylibparted as parted

import cairn
from cairn import Options
from cairn.sysdefs.linux import Shared



def getClass():
	return List()


class List(object):

	def scanPVs(self, sysdef):
		cmd = sysdef.info.get("env/tools/pvscan")
		(status, output) = commands.getstatusoutput(cmd)
		if (status != 0):
			raise cairn.Exception("Failed to scan Physical Volumes: %s" % output)
		pvs = []
		pvsElem = sysdef.info.getElem("hardware/lvm-cfg/pvs")
		for line in output.split("\n"):
			line = line.strip()
			if re.match("^PV /dev/*", line):
				words = line.split()
				pvs.append(words[1])
				elem = pvsElem.createElem("pv", words[1], True)
				elem.setAttr("vg", words[3])
		return pvs


	def scanVGs(self, sysdef):
		cmd = sysdef.info.get("env/tools/vgscan")
		(status, output) = commands.getstatusoutput(cmd)
		if (status != 0):
			raise cairn.Exception("Failed to scan Volume Groups: %s" % output)
		vgs = []
		vgsElem = sysdef.info.getElem("hardware/lvm-cfg/vgs")
		for line in output.split("\n"):
			line = line.strip()
			if re.match("Found volume group ", line):
				words = line.split("\"")
				vgs.append(words[1])
				vgsElem.createElem("vg", words[1], True)
		return vgs


	def scanLVs(self, sysdef):
		cmd = sysdef.info.get("env/tools/lvscan")
		(status, output) = commands.getstatusoutput(cmd)
		if (status != 0):
			raise cairn.Exception("Failed to scan Logical Volumes: %s" % output)
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
		return lvs


	def defineDevices(self, sysdef):
		lvs = sysdef.info.getElems("hardware/lvm-cfg/lvs/lv")
		for vg in sysdef.info.getElems("hardware/lvm-cfg/vgs/vg"):
			vgname = vg.getText()
			vgdev = "/dev/" + vgname
			devElem = sysdef.info.createDeviceElem(vgname)
			devElem.setChild("device", vgdev)
			devElem.setChild("type", "lvm")
			dlabel = sysdef.info.createDiskLabelElem(devElem)
			dlabel.setChild("type", "lvm")
			count = 1
			for lv in lvs:
				if lv.getAttr("vg") != vgname:
					continue
				fulldev = "%s/%s" % (vgdev, lv.getText())
				partElem = sysdef.info.createPartitionElem(devElem,
														   "%d" % count)
				partElem.setChild("device", fulldev)
				empty = True
				try:
					pdev = parted.PedDevice(fulldev)
					pdisk = pdev.diskNew()
					pparts = pdisk.getPartitions()
					Shared.definePartition(sysdef, devElem, partElem,
										   pparts[0])
					empty = False
				except Exception, err:
					cairn.error("%s" % err)
				if empty:
					partElem.setChild("empty", "true")
				partElem.setChild("type", "loop")
				count = count + 1
		return True


	def run(self, sysdef):
		if Options.get("no-lvm") or not sysdef.info.get("env/tools/lvm"):
			cairn.log("Skipping LVM check")
			return True
		cairn.log("Checking for LVM volumes")
		pvs = self.scanPVs(sysdef)
		cairn.info("  Found PVs: %s" % " ".join(pvs))
		vgs = self.scanVGs(sysdef)
		cairn.info("  Found VGs: %s" % " ".join(vgs))
		lvs = self.scanLVs(sysdef)
		cairn.info("  Found LVs: %s" % " ".join(lvs))
		self.defineDevices(sysdef)
		return True
