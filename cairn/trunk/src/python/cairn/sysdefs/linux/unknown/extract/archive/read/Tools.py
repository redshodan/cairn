"""linux.unknown.extract.archive.read.Tools Module"""


import cairn.sysdefs.linux.unknown.archive.read.Tools as tmpl


def getClass():
	return Tools()


class Tools(tmpl.Tools):

	def setTarCmd(self, sysdef):
		cmd = "%s --preserve --numeric-owner -X %s  -C %s -Sxpf -" % \
			  (sysdef.info.get("env/tools/tar"),
			   sysdef.info.get("archive/excludes-file"),
			   sysdef.info.get("env/mountdir"))
		sysdef.info.setChild("archive/archive-tool-cmd", cmd)
		return


	def setStarCmd(self, sysdef):
		raise cairn.Exception("Complete me!")
