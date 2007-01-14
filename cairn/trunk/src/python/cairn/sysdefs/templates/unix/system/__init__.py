"""templates.unix.system Module"""


import cairn
from cairn import Options



def getSubModuleString(sysdef):
	str = "OS; Arch; Machine; Paths; drives; "
	if Options.get("command") == "copy":
		str = str + "partitions; BootLoader; "
	str = str + "Summary; verify"
	return str
