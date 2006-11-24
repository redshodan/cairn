"""linux.unknown.system Module"""



import cairn
from cairn import Options
from cairn.sysdefs.templates.unix import system


def getSubModuleString(sysdef):
	mods = system.getSubModuleString(sysdef)
	if Options.get("program") == "copy":
		return mods.replace("drives", "drives; lvm")
		#return mods.replace("drives", "drives; md; lvm")
	else:
		return mods
