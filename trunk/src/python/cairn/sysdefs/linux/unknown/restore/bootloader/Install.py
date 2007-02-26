"""linux.unknown.restore.bootloader.Install Module"""



import cairn
from cairn import Options
import cairn.sysdefs.templates.unix.restore.bootloader.Install as tmpl



def getClass():
	return Install()


class Install(tmpl.Install):

	def run(self, sysdef):
		if ((Options.get("boot") == "grub") or
			(sysdef.readInfo.get("machine/bootloader/type") == "grub")):
			sysdef.moduleList.insertAfterMe("bootloader.grub")
		elif ((Options.get("boot") == "lilo") or
			  (sysdef.readInfo.get("machine/bootloader/type") == "lilo")):
			sysdef.moduleList.insertAfterMe("bootloader.lilo")
		else:
			cairn.warn("This image has an unknown bootloader. No boot loader has been installed. You will have to manually install the bootloader or else this machine will be unbootable")
		return True
