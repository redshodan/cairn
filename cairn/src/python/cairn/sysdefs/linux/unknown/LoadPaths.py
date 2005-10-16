"""Unknown Linux system definitions"""


import cairn
from cairn import sysdefs


# If including this module, override these variables before calling
# run.
PATH = "/sbin:/usr/sbin:/bin:/usr/bin"
BINS = { "PART_TOOL" : "sfdisk", "ARCHIVE_TOOL" : "tar" }


def run(sysdef, sysinfo):
	sysinfo.set("PATH", PATH)
	for key, val in BINS.iteritems():
		sysinfo.set(key, sysdefs.findFileInPath(PATH, val))
		if not sysinfo.get(key):
			raise cairn.Exception(cairn.ERR_BINARY, "Failed to find required binary: %s" % val)
	return True
