"""linux.unknown.hardware.Drives Module"""


import cairn


def getClass():
	return Drives()


class Drives(object):
	def run(self, sysdef):
		ver = sysdef.info.get("os/version-short")
		if ver == "2.4":
			sysdef.moduleList.insertAfterMe("cairn.sysdefs.linux.unknown.hardware.Drives.Drives2_4")
		if ver == "2.6":
			sysdef.moduleList.insertAfterMe("cairn.sysdefs.linux.unknown.hardware.Drives.Drives2_6")
		return True
