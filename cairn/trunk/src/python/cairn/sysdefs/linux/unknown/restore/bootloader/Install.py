"""linux.unknown.restore.bootloader.Install Module"""



import cairn.sysdefs.templates.unix.restore.bootloader.Install as tmpl



def getClass():
	return Install()


class Install(tmpl.Install):

	def run(self, sysdef):
		return False
