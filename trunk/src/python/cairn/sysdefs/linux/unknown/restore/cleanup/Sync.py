"""linux.unknown.restore.cleanup.Sync"""



import cairn
import cairn.sysdefs.templates.unix.restore.cleanup.Sync as tmpl



def getClass():
	return Sync()



class Sync(tmpl.Sync):

	def run(self, sysdef):
		cmd = sysdef.info.get("env/tools/sync")
		if cmd:
			cairn.verbose("Syncing drives")
			cairn.run(cmd, "Failed to sync drives")
		return True
