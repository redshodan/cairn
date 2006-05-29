"""linux.unknown.setup.PartDrives Module"""


import os
import commands
import re
import tempfile

import cairn
import cairn.sysdefs.templates.unix.restore.setup.PartDrives as tmpl


def getClass():
	return PartDrives()


class PartDrives(tmpl.PartDrives):

	def partitionDrive(self, sysdef, drive):
		cfgFile = self.writePartCfg(sysdef, drive)
		device = drive.get("mapped-device")
		cmd = "%s --force %s < %s" % (sysdef.info.get("env/tools/part"), device,
									  cfgFile)
		ret = commands.getstatusoutput(cmd)
		if ret[0] != 0:
			msg = "Failed to run %s to partition drive %s: %s" % \
				  (sysdef.info.get("env/tools/part"), device, ret[1])
			raise cairn.Exception(msg)
		cairn.verbose(ret[1])
		return


	def writePartCfg(self, sysdef, drive):
		cfgFile = tempfile.mkstemp("", "cairn-")
		cairn.addFileForCleanup(cfgFile[1])
		contents = "%s\n" % drive.get("part-tool-cfg")
		os.write(cfgFile[0], contents)
		os.close(cfgFile[0])
		return cfgFile[1]