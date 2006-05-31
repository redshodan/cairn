"""templates.unix.restore.cleanup.UnMountParts - """


import cairn
from cairn.sysdefs.linux import Shared


def getClass():
	return UnMountParts()


class UnMountParts(object):

	def run(self, sysdef):
		Shared.unmountAll(sysdef)
		return True
