"""linux.unknown.system.drives.List Module"""


import re


import cairn
import cairn.sysdefs.templates.unix.system.drives.List as tmpl


def getClass():
	return List()


class List(tmpl.List):

	def run(self, sysdef):
		ver = sysdef.info.get("os/version-short")
		if ver == "2.4":
			sysdef.moduleList.insertAfterMe("system.drives.List2_4")
		if ver == "2.6":
			sysdef.moduleList.insertAfterMe("system.drives.List2_6")
		return True

