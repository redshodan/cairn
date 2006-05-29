"""linux.Shared Module"""


import commands

from cairn.sysdefs.linux.Constants import *


##
## Shared utility functions
##


def matchDevice(device, deviceRegexp = None):
	if not deviceRegexp:
		deviceRegexp = DEVICE_RE
	for pattern in deviceRegexp:
		if pattern.match(device):
			return True
	return False


def mount(sysdef, device, dir, opts = ""):
	cairn.log("Mounting %s on %s" % (device, dir))
	cmd = "%s %s %s %s" % (sysdef.info.get("env/tools/mount"), opts, device, dir)
	ret = commands.getstatusoutput(cmd)
	if ret[0] != 0:
		raise cairn.Exception("Failed to mount %s on %s: %s" %
							  (device, dir, ret[1]))
	return
