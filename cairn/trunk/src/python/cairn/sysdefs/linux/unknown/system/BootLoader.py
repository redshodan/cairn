"""linux.unknown.system.BootLoader Module"""



import cairn
from cairn import Options
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
		if mbr.find("GRUB") >= 0:
			return True
		return False


	def checkLILO(self, sysdef, mbr):
		if mbr.find("lilo") >= 0:
			return True
		return False


	def run(self, sysdef):
		if Options.get("boot"):
			cairn.log("User choose bootloader: %s" % Options.get("boot"))
			sysdef.info.setChild("machine/bootloader/type", Options.get("boot"))
			return True
		mbr = self.readMBR(sysdef)
		if not mbr:
			return True
		if self.checkGRUB(sysdef, mbr):
			cairn.log("Installed bootloader: GRUB")
			sysdef.info.setChild("machine/bootloader/type", "grub")
		elif self.checkLILO(sysdef, mbr):
			cairn.log("Installed bootloader: LILO")
			sysdef.info.setChild("machine/bootloader/type", "lilo")
		else:
			cairn.log("Installed bootloader: unknown")
			sysdef.info.setChild("machine/bootloader/type", "unknown")
		return True
