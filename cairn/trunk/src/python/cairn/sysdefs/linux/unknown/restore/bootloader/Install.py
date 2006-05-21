"""templates.unix.restore.bootloader.Install Module"""


import cairn.sysdefs.linux.unknown.restore.bootloader.Install as tmpl



def getClass():
	return Install()


class Install(tmpl.Install):

	def run(self, sysdef):
		return False
