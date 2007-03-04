"""linux.unknown.restore.cleanup.UnMountParts"""


import cairn
from cairn.sysdefs.linux import Shared
from cairn import Options
import cairn.sysdefs.templates.unix.restore.cleanup.UnMountParts as tmpl

def getClass():
	return UnMountParts()


class UnMountParts(tmpl.UnMountParts):

	def run(self, sysdef):
		if not Options.get("no-cleanup"):
			Shared.unmountAll(sysdef)
		return True
