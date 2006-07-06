"""templates.unix.archive.write Module"""


import cairn
from cairn import Options



def getSubModuleString(sysdef):
	str = "Prep; Tools; Excludes; %s; PrepMeta; WriteMeta; RunArchiver; FinalizeMeta;"
	if Options.get("quick"):
		str = str % "EstimateSizeQuick"
	else:
		str = str % "EstimateSize"
	return str
