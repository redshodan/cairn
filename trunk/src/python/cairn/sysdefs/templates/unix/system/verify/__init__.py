"""templates.unix.system.verify Module"""



import cairn
from cairn import Options


def getSubModuleString(sysdef):
	if Options.get("no-verify"):
		return None
	else:
		return "OS; Arch; Machine; BootLoader; Summary;"
