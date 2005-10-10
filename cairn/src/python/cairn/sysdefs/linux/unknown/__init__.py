"""Unknown Linux system definitions"""


import sys
import os
import re

import cairn
import cairn.Options
from cairn import sysdefs
from cairn.sysdefs.SystemInfo import *



def getPlatform():
	return Unknown()



class Unknown:
	def __init__(self):
		return


	def matchPartial(self):
		return False


	def matchExact(self):
		return False


	def name(self):
		return "Unknown"
	

	def getPath(self):
		return "/sbin:/usr/sbin:/bin:/usr/bin"


	def getBins(self):
		return { "PART_TOOL" : "sfdisk", "ARCHIVE_TOOL" : "tar" }


	def load(self):
		return


	def loadInfo(self):
		info = SystemInfo()
		info.set("OS", "Linux")
		self.loadOS(info)
		self.loadArch(info)
		self.loadPaths(info)
		return info


	def loadOS(self, info):
		sysname, nodename, release, version, machine = os.uname()
		arr = release.split("-")
		nums = arr[0].split(".")
		info.set("OS_VER", arr[0])
		info.set("OS_VER_SHORT", "%s.%s" % (nums[0], nums[1]))
		info.set("OS_VER_STR", release)
		info.set("OS_DISTRO", self.name())
		return


	def loadArch(self, info):
		sysname, nodename, release, version, machine = os.uname()
		info.set("CPU", machine)
		if re.compile("i[3456]86").match(machine):
			info.set("ARCH", "i386")
		elif ((machine == "ia64") or (machine == "x86_64") or
			  (machine == "ppc")):
			info.set("ARCH", machine)

		modelNameRE = re.compile("^model name")
		cpuinfo = file("/proc/cpuinfo", "r")
		for line in cpuinfo.readlines():
			if modelNameRE.match(line):
				arr = line.split(": ")
				info.set("CPU_STR", arr[1])
		cpuinfo.close()
		return


	def loadPaths(self, info):
		path = self.getPath()
		info.set("PATH", path)
		for key, val in self.getBins().iteritems():
			info.set(key, sysdefs.findFileInPath(path, val))
			if not info.get(key):
				raise cairn.Exception(cairn.ERR_BINARY, "Failed to find required binary: %s" % val)
		return


	def printSummary(self):
		print "System definition:  %s Linux" % (self.name())
		return
