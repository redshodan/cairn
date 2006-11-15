"""linux.unknown.system.drives.ListLVM Module"""


import re
import commands


import cairn
from cairn import Options
from cairn.sysdefs.linux import Shared



def getClass():
	return ListLVM()


class ListLVM(object):

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
				pvsElem.createElem("pv", words[1], True)
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
				lv = words[1].strip("'")
				lv = lv[5:]
				lvs.append(lv)
				lvsElem.createElem("lv", lv, True)
		return lvs


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
		return True
