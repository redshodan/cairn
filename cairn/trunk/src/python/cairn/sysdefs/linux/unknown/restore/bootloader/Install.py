"""linux.unknown.restore.bootloader.Install Module"""



import cairn.sysdefs.templates.unix.restore.bootloader.Install as tmpl



def getClass():
	return Install()


class Install(tmpl.Install):

	def run(self, sysdef):
		if sysdef.readInfo.get("machine/bootloader") == "grub"):
			sysdef.moduleList.insertAfterMe("bootloader.grub")
		elif sysdef.readInfo.get("machine/bootloader") == "lilo"):
			sysdef.moduleList.insertAfterMe("bootloader.lilo")
		return False
