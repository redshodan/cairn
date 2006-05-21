"""templates.unix.archive.read.Tools Module"""


import cairn.sysdefs.templates.unix.archive.Tools as tmpl


#
# This exists soley to disable the setDiskUsageCmd since it is not
# used for archive reading. The real system definition still needs to
# override the setArchiveCmd and setZipCmd functions.
#


def getClass():
	return Tools()


class Tools(tmpl.Tools):

	def setDiskUsageCmd(self, sysdef):
		return True
