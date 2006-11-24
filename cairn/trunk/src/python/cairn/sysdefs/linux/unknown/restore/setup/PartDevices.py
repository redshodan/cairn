"""linux.unknown.setup.PartDevices Module"""


import cairn
import cairn.sysdefs.templates.unix.restore.setup.PartDevices as tmpl


def getClass():
	return PartDevices()


class PartDevices(tmpl.PartDevices):

	def run(self, sysdef):
		sysdef.moduleList.insertAfterMe("restore.setup.PartDevicesParted")
		return True
