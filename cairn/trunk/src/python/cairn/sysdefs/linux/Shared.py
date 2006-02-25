"""linux.Shared Module"""



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
