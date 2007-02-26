"""templates.unix.restore.setup.PartDevices Module"""


import cairn



def getClass():
	return PartDevices()


class PartDevices(object):

	def run(self, sysdef):
		return True
