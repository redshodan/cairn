"""templates.unix.setup.PartDrives Module"""


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
		cmd = "%s -l %s" % (sysdef.info.get("env/tools/part"),
							drive.get("device"))
		if ret[0] != 0:
			msg = "Failed to run %s to partition drive %s: %s" % \
				  (sysdef.info.get("env/tools/part"), drive.get("device"),
				   ret[1])
			raise cairn.Exception(msg)
		return


	def writePartCfg(self, sysdef, drive):
		cfgFile = tempfile.mkstemp(None, "cairn-")
		cairn.addfileForCleanup(cfgFile[1])
		cfgFile[0].write(drive.get("part-tool-cfg"))
		cfgFile[0].close()
		return cfgFile[1]
