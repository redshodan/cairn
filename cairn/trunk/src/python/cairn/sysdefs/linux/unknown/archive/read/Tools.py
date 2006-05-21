"""linux.unknown.archive.read.Tools Module"""


import cairn.sysdefs.linux.unknown.archive.Tools as tmpl


def getClass():
	return Tools()


class Tools(tmpl.Tools):

	def setTarCmd(self, sysdef):
		cmd = "%s --preserve --numeric-owner -X %s -PSxpf - -C %s" % \
			  (sysdef.info.get("env/tools/tar"),
			   sysdef.info.get("archive/excludes-file")
			   sysdef.info.get("env/mountdir"))
		sysdef.info.setChild("archive/archive-tool-cmd", cmd)
		return


	def setStarCmd(self, sysdef):
		raise cairn.Exception("Complete me!")


	def setBzip2Cmd(self, sysdef):
		sysdef.info.setChild("archive/zip-tool-cmd",
							 "%s -dc" % (sysdef.info.get("env/tools/bzip2")))
		return


	def setGzipCmd(self, sysdef):
		sysdef.info.setChild("archive/zip-tool-cmd",
							 "%s -dc" % (sysdef.info.get("env/tools/gzip")))
		return


	# This exists soley to disable the setDiskUsageCmd since it is not used
	def setDiskUsageCmd(self, sysdef):
		return True
