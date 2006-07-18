"""linux.unknown.restore.cleanup.Sync"""


import commands

import cairn
import cairn.sysdefs.templates.unix.restore.cleanup.Sync as tmpl



def getClass():
	return Sync()



class Sync(tmpl.Sync):

	def run(self, sysdef):
		cmd = sysdef.info.get("env/tools/sync")
		if cmd:
			cairn.verbose("Syncing drives")
			ret = commands.getstatusoutput(cmd)
			if ret[0] != 0:
				raise cairn.Exception("Failed to sync drives: %s" % ret[1])
		return True
