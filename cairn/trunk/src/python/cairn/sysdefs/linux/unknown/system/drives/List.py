"""linux.unknown.system.drives.List Module"""


import re


import cairn
import cairn.sysdefs.templates.unix.system.drives.List as tmpl


def getClass():
	return List()


class List(tmpl.List):

	def run(self, sysdef):
		sysdef.moduleList.insertAfterMe("system.drives.ListDrives;" +
                                        "system.drives.ListMD;" +
                                        "system.drives.ListMDP;" +
                                        "system.drives.ListLVM;" +
										"system.drives.LVMBackup")
		return True
