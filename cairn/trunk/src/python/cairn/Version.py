"""cairn.Version - Version handling"""


from cairn import Logging



MAJOR = 0
MINOR = 1
MAINT = 0
SVNREV = 0
DEVEL = True



def toString():
	str = "%d.%d.%d revision %d" % (MAJOR, MINOR, MAINT, SVNREV)
	if DEVEL:
		return str + " DEVEL"
	else:
		return str


def printVer():
	Logging.error.log(Logging.CRITICAL, "CAIRN version: %s" % toString())
	return
