"""linux.unknown.system.partitions Module"""


import cairn
from cairn import Options
from cairn.sysdefs.templates.unix.system import partitions


def getSubModuleString(sysdef):
	mods = partitions.getSubModuleString(sysdef)
	return mods.replace("FSTab;", "VolumeID; FSTab;")
