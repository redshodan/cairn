"""linux.Shared - Common linux code"""


import commands

from cairn.sysdefs.linux.Constants import *
from cairn.sysdefs.templates.unix.misc Mounts


##
## Shared utility functions
##


mountedFS = []


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
	mountedFS.append(dir)
	return


def unmountAll(sysdef):
	mountedFS.sort()
	for mount in mountedFS:
		cairn.log("Umounting %s" % mount)
		cmd = "%s %s" % (sysdef.info.get("env/tools/unmount"), dir)
		ret = commands.getstatusoutput(cmd)
		if ret[0] != 0:
			raise cairn.Exception("Failed to unmount %s %s" % (dir, ret[1]))
	return
