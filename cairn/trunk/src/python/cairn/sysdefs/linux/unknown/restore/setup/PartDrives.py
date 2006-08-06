"""linux.unknown.setup.PartDrives Module"""


import cairn
import cairn.sysdefs.templates.unix.restore.setup.PartDrives as tmpl


def getClass():
	return PartDrives()


class PartDrives(tmpl.PartDrives):

	def run(self, sysdef):
		sysdef.info.insertAfterMe("restore.setup.PartDrivesParted")
		return True
