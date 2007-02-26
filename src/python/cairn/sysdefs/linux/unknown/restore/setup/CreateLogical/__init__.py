"""templates.unix.restore.setup.CreateLogical Module"""


import cairn
from cairn import Options



def getSubModuleString(sysdef):
	str = "ModuleProbe; CreateMD; CreateLVM;"
	return str
