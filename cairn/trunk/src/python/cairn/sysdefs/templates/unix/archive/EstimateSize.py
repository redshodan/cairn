"""templates.unix.copy.EstimateSize Module"""


import commands
import re
import fnmatch

import cairn
from cairn import Options



def getClass():
	return EstimateSize()



class EstimateSize(object):

	def findTotalSize(self, sysdef):
		totalSize = long(0)
		for drive in sysdef.info.getElems("hardware/drive"):
			for partition in sysdef.info.getElems("partition", drive):
				space = sysdef.info.getElem("space", partition)
				if space:
					used = sysdef.info.get("used", space)
					totalSize = totalSize + long(used)
		return totalSize


	def collateExcludes(self, sysdef):
		excludes = sysdef.info.getElems("archive/excludes/exclude")
		if not excludes:
			return 0
		ignored_fs = []
		user = []
		for exclude in excludes:
			if exclude.getAttribute("type") == "ignored_fs":
				ignored_fs.append(sysdef.info.getText(exclude))
			if exclude.getAttribute("type") == "user":
				user.append(sysdef.info.getText(exclude))
		good = []
		for userX in user:
			add = True
			userX = userX.rstrip("*")
			for ignored in ignored_fs:
				ignored = ignored.rstrip("*")
				if userX.startswith(ignored):
					add = False
					break
			if add:
				good.append(userX)
				cairn.verbose("User requested exclude of: %s" % (userX))
		return good


	def findExcludedSize(self, sysdef, goodExcludes):
		cmd = sysdef.info.get("archive/diskusage-tool-cmd")
		excludeSize = 0
		for exclude in goodExcludes:
			ret = commands.getstatusoutput("%s %s" % (cmd, exclude))
			if ret[0] != 0:
				raise cairn.Exception("Unable to run du: %s" % (ret[1]))
			arr = ret[1].split()
			excludeSize = excludeSize + int(arr[0])
			cairn.verbose("Exclude %s contains %d bytes" % (exclude, int(arr[0])))
		return excludeSize


	def run(self, sysdef):
		if Options.get("nosize"):
			return True
		totalSize = self.findTotalSize(sysdef)
		goodExcludes = self.collateExcludes(sysdef)
		excludedSize = self.findExcludedSize(sysdef, goodExcludes)
		sysdef.info.set("archive/real-size", "%d" % (totalSize))
		sysdef.info.set("archive/adjusted-size", "%d" % (totalSize - excludedSize))
		cairn.verbose("Total size: %d" % (totalSize))
		cairn.verbose("Total excluded size: %d" % (excludedSize))
		cairn.verbose("Adjusted size: %d" % (totalSize - excludedSize))
		return True
