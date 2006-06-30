"""linux.unknown.system.partitions.List Module"""


import commands
import re
import tempfile
import os

import cairn
import cairn.sysdefs.templates.unix.system.partitions.List as tmpl


def getClass():
	return List()


#
# For PC's it seems the smallest unit of space is a sector with is 512 bytes in
# size. Work with that assumption.
#


class List(tmpl.List):

	def run(self, sysdef):
		cairn.log("Checking partitions")
		for drive in sysdef.info.getElems("hardware/drive"):
			self.definePartitions(sysdef, drive)
		return True


	def definePartitions(self, sysdef, drive):
		cfgFile = tempfile.mkstemp("", "cairn-")
		cairn.addFileForCleanup(cfgFile[1])
		cmd = "%s -uS -d %s > %s" % (sysdef.info.get("env/tools/part"),
									 drive.get("device"), cfgFile[1])
		ret = commands.getstatusoutput(cmd)
		if ret[0] != 0:
			msg = "Failed to run %s to find drive information:\n" % sysdef.info.get("env/tools/part")
			raise cairn.Exception(msg + ret[1])
		if len(ret[1]) > 0:
			cairn.verbose("sfdisk output: %s" % ret[1])
		content = os.read(cfgFile[0], 1000000)
		os.close(cfgFile[0])
		drive.setChild("part-tool-cfg", content)
		partNum = 1
		for line in content.split("\n"):
			if line.startswith("/dev/"):
				if line.endswith("Id= 0"):
					partNum = partNum + 1
					continue
				try:
					part = sysdef.info.createPartitionElem(drive, "%d" % partNum)
					arr = line.split(":")
					part.setChild("device", arr[0].strip())
					arr = arr[1].split(",")
					word = arr[0].split("=")
					part.setChild("start", word[1].strip())
					word = arr[1].split("=")
					part.setChild("size", word[1].strip())
					word = arr[2].split("=")
					part.setChild("type", word[1].strip())
					partNum = partNum + 1
				except Exception, err:
					raise cairn.Exception("Failed to parse sfdisk output: %s" % err)
		return
