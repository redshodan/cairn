"""linux.unknown.system Module"""



import cairn
from cairn.sysdefs.templates.unix import system



def getSubModuleString(sysdef):
	mods = system.getSubModuleString(sysdef)
	return mods.replace("drives", "drives; lvm")
	#return mods.replace("drives", "drives; md; lvm")
