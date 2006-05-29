"""linux.unknown.restore.bootloader.grub.PrepMounts Module"""


import os.path

import cairn
from cairn.sysdefs.linux import Shared



def getClass():
	return PrepMounts()


class PrepMounts(object):

	def run(self, sysdef):
		mdir = sysdef.info.get("env/mountdir")
		Shared.mount(sysdef, "/proc", os.path.join(mdir, "proc"), "--bind")
		Shared.mount(sysdef, "/dev", os.path.join(mdir, "dev"), "--bind")
		if sysdef.info.get("os/version-short") == "2.6":
			Shared.mount(sysdef, "/sys", os.path.join(mdir, "sys"), "--bind")
		return
