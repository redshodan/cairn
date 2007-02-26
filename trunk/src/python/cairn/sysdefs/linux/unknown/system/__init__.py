"""linux.unknown.system Module"""



import cairn
from cairn import Options
from cairn import sysdefs
from cairn.sysdefs.templates.unix import system


def getSubModuleString(sysdef):
	mods = system.getSubModuleString(sysdef)
	if Options.get("command") == "copy":
		mods = mods.replace("drives; partitions", "drives; md; lvm; partitions")
	if (not sysdefs.getCommand().disableLogging() and
		((Options.get("command") == "copy") or
		 (Options.get("command") == "restore"))):
		mods = "%s;%s" % ("Klog", mods)
	return mods
