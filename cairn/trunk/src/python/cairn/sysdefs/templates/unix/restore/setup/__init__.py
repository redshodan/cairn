"""templates.unix.restore.setup Module"""


import cairn
from cairn import Options



def getSubModuleString(sysdef):
	str = "VerifyTools; MatchUpDrives; PartDrives; MakeFS; MountParts; "
	return str
