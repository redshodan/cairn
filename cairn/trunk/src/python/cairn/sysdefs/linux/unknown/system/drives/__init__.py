"""linux.unknown.system.drives Module"""


import re

import cairn



def getSubModuleString(sysdef):
	ver = sysdef.info.get("os/version-short")
	if ver == "2.4":
		return "cairn.sysdefs.linux.unknown.system.drives.List2_4"
	if ver == "2.6":
		return "cairn.sysdefs.linux.unknown.system.drives.List2_6"
	return ""



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
