"""linux.unknown.system.BootLoader Module"""



import cairn
import cairn.sysdefs.templates.unix.system.BootLoader as tmpl



def getClass():
	return BootLoader()



class BootLoader(tmpl.BootLoader):

	def readMBR(self, sysdef):
		drives = sysdef.info.getElems("hardware/drive")
		if not drives:
			cairn.log("No drives found to check for bootloader")
			return None
		dev = drives[0].get("device")
		try:
			mbr = file(dev, "r")
			buf = mbr.read(512)
			mbr.close()
			return buf
		except Exception, err:
			raise cairn.Exception("Failed to read MBR from drive %s: %s" % (dev,
																			err))
		return None


	def checkGRUB(self, sysdef, mbr):
		if mbr.find("GRUB"):
			return True
		return False


	def checkLILO(self, sysdef, mbr):
		if mbr.find("lilo"):
			return True
		return False


	def run(self, sysdef):
		mbr = self.readMBR(sysdef)
		if not mbr:
			return True
		if self.checkGRUB(sysdef, mbr):
			cairn.log("Installed bootloader: GRUB")
			sysdef.info.setChild("os/bootloader", "grub")
		elif self.checkLILO(sysdef, mbr):
			cairn.log("Installed bootloader: LILO")
			sysdef.info.setChild("os/bootloader", "lilo")
		else:
			cairn.log("Installed bootloader: unknown")
			sysdef.info.setChild("os/bootloader", "unknown")
		return True
