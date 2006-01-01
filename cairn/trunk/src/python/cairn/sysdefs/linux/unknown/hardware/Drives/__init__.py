"""linux.unknown.hardware.Drives Module"""


import re


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


##
## Shared utility functions
##

__deviceRegexp = [re.compile("hd[a-z]+"), re.compile("sd[a-z]+"),
				  re.compile("ubd[a-z]+")]

def matchDevice(device, deviceRegexp = None):
	if not deviceRegexp:
		deviceRegexp = __deviceRegexp
	for pattern in deviceRegexp:
		if pattern.match(device):
			return True
	return False
