"""templates.unix.restore.cleanup.UnMountParts - """


import cairn
from cairn.sysdefs.linux import Shared
from cairn import Options


def getClass():
	return UnMountParts()


class UnMountParts(object):

	def run(self, sysdef):
		if not Options.get("nocleanup"):
			Shared.unmountAll(sysdef)
		return True
