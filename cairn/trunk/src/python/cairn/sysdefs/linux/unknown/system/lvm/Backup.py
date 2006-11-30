"""linux.unknown.system.drives.LVMBackup Module"""


import os
import re

import cairn
from cairn import Options
from cairn.sysdefs.linux import Shared



def getClass():
	return LVMBackup()


class LVMBackup(object):

	def backupVG(self, sysdef, dir, vgname):
		cmd = "%s -f %s %s" % (sysdef.info.get("env/tools/vgcfgbackup"),
							   os.path.join(dir, "%s"), vgname)
		cairn.run(cmd, "Failed to backup Logical Volumes")
		vgfile = file(os.path.join(dir, vgname))
		contents = vgfile.read()
		vgfile.close()
		bkups = sysdef.info.getElem("hardware/lvm-cfg/vg-backups")
		vg = bkups.createElem("vg", None, True)
		vg.setAttribute("name", vgname)
		vg.set(contents)
		return


	def run(self, sysdef):
		if Options.get("no-lvm") or not sysdef.info.get("env/tools/lvm"):
			cairn.log("Skipping LVM backup")
			return True
		cairn.log("Backing up LVM volumes")
		try:
			dir = cairn.mkdtemp("cairn-lvm-backup")
		except Exception, err:
			raise cairn.Exception("Failed to create temporary directory: " +
								  "cairn-lvm-backup")
		vgs = sysdef.info.getElems("hardware/lvm-cfg/vgs/vg")
		for vg in vgs:
			self.backupVG(sysdef, dir, vg.getText())
		return True
