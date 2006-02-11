"""linux.archive.Tools Module"""



import cairn
import cairn.sysdefs.templates.unix.archive.Tools as tmpl


def getClass():
	return Tools()


ARCHIVE = ["tar", "star"]
ZIP = ["bzip2", "gzip"]


class Tools(tmpl.Tools):

	def setArchiveCmd(self, sysdef):
		method = sysdef.info.get("archive/archive-tool")
		if method == "env/tools/tar":
			self.setTarCmd(sysdef)
		elif method == "env/tools/star":
			self.setStarCmd(sysdef)
		else:
			raise cairn.Exception("Unknown archive method choosen: " + method)
		return True


	def setTarCmd(self, sysdef):
		cmd = "%s --preserve --numeric-owner -X %s -PScpf - /" % \
			  (sysdef.info.get("env/tools/tar"),
			   sysdef.info.get("archive/excludes-file"))
		sysdef.info.set("archive/archive-tool-cmd", cmd)
		return


	def setStarCmd(self, sysdef):
		raise cairn.Exception("Complete me!")


	def setZipCmd(self, sysdef):
		method = sysdef.info.get("archive/zip-tool")
		if method == "env/tools/bzip2":
			self.setBzip2Cmd(sysdef)
		elif method == "env/tools/gzip":
			self.setGzipCmd(sysdef)
		else:
			raise cairn.Exception("Unknown zip method choosen: " + method)
		return True


	def setBzip2Cmd(self, sysdef):
		sysdef.info.set("archive/zip-tool-cmd",
						"%s -zc" % (sysdef.info.get("env/tools/bzip2")))
		return


	def setGzipCmd(self, sysdef):
		sysdef.info.set("archive/zip-tool-cmd",
						"%s -c" % (sysdef.info.get("env/tools/gzip")))
		return


	def setDiskUsageCmd(self, sysdef):
		sysdef.info.set("archive/diskusage-tool-cmd",
						"%s -s" % (sysdef.info.get("env/tools/diskusage")))
		return True
