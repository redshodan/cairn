"""linux.unknown.restore.setup.VerifyTools Module"""


import cairn
from cairn.sysdefs.linux import Constants
import cairn.sysdefs.templates.unix.restore.setup.VerifyTools as tmpl


def getClass():
	return VerifyTools()


class VerifyTools(tmpl.VerifyTools):

	def run(self, sysdef):
		for drive in sysdef.info.getElems("hardware/drive"):
			for part in drive.getElems("partition"):
				fsType = part.getChild("fs-type")
				if fsType not in Constants.FS_MAP:
					raise cairn.Exception("Unknown filesystem type %s for %s found in archive" % (fsType, part.getChild("device")))
				if not sysdef.info.get(Constants.FS_MAP[fsType]):
					raise cairn.Exception("Failed to find mkfs for filesystem type %s" % (fstype))
		return True
