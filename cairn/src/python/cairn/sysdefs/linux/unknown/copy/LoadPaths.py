"""Unknown Linux system definitions"""


import cairn
import cairn.sysdefs as sysdefs


__PATH = "/sbin:/usr/sbin:/bin:/usr/bin"
__BINS = { "PART_TOOL" : "sfdisk", "ARCHIVE_TOOL" : "tar" }


def run(sysdef, sysinfo):
	sysdefs.findPaths(sysdef, sysinfo, __PATH, __BINS)
	return True
