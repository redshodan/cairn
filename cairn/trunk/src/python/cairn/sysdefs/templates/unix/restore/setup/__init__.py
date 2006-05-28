"""templates.unix.restore.setup Module"""


import cairn
from cairn import Options



def getSubModuleString(sysdef):
	str = "VerifyTools; MatchDrives; PartDrives; MakeFS; MountParts; "
	return str
