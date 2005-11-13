"""Generic UNIX system definitions"""


import cairn
import cairn.sysdefs as sysdefs


# If including this module, supply variables like these when calling
# findPaths()
__PATH = "/sbin:/usr/sbin:/bin:/usr/bin"
__BINS = { "PART_TOOL" : "sfdisk", "ARCHIVE_TOOL" : "tar" }


def run(sysdef, sysinfo):
	sysdefs.findPaths(sysdef, sysinfo, __PATH, __BINS)
	return True

