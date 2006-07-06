"""cairn.Version - Version handling"""



MAJOR = 0
MINOR = 1
MAINT = 0
SVNREV = 0
DEVEL = True



def toString():
	str = "%d.%d.%d SVN %d" % (MAJOR, MINOR, MAINT, SVNREV)
	if DEVEL:
		return str + " DEVEL"
	else:
		return str


def printVer():
	from cairn import Logging
	Logging.display.log(Logging.INFO, "CAIRN version: %s" % toString())
	return
