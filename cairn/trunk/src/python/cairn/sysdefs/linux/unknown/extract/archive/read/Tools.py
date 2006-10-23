"""linux.unknown.extract.archive.read.Tools Module"""


from cairn import Options
import cairn.sysdefs.linux.unknown.archive.read.Tools as tmpl


def getClass():
	return Tools()


class Tools(tmpl.Tools):

	def setTarCmd(self, sysdef):
		if Options.get("restore-opts"):
			cmd = "%s --preserve --numeric-owner -X %s -C %s -Sxpf -" % \
				  (sysdef.info.get("env/tools/tar"),
				   sysdef.info.get("archive/excludes-file"),
				   sysdef.info.get("env/mountdir"))
		else:
			if Options.getExtraOpts():
				cmd = "%s -f - %s" % (sysdef.info.get("env/tools/tar"),
									  " ".join(Options.getExtraOpts()))
			else:
				cmd = "%s -f -" % (sysdef.info.get("env/tools/tar"))
		sysdef.info.setChild("archive/archive-tool-cmd", cmd)
		return


	def setStarCmd(self, sysdef):
		raise cairn.Exception("Complete me!")
