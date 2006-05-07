"""templates.unix.archive Module"""


import cairn
from cairn import Options



def getSubModuleString(sysdef):
	str = "FileName; Tools; Excludes; %s; PrepMeta; WriteMeta; CreateArchive; FinalizeMeta;"
	if Options.get("quick"):
		str = str % "EstimateSizeQuick"
	else:
		str = str % "EstimateSize"
	return str
