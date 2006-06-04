"""linux.unknown.restore.bootloader.Install Module"""



import cairn
import cairn.sysdefs.templates.unix.restore.bootloader.Install as tmpl



def getClass():
	return Install()


class Install(tmpl.Install):

	def run(self, sysdef):
		if sysdef.readInfo.get("machine/bootloader/type") == "grub":
			sysdef.moduleList.insertAfterMe("bootloader.grub")
		elif sysdef.readInfo.get("machine/bootloader/type") == "lilo":
			sysdef.moduleList.insertAfterMe("bootloader.lilo")
		else:
			cairn.warn("This image has an unknown bootloader. No boot loader has been installed. You will have to manually install the bootloader or else this machine will be unbootable")
		return True
