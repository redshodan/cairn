"""linux.unknown.restore.setup.VerifyTools Module"""


import cairn
from cairn.sysdefs.linux import Constants
import cairn.sysdefs.templates.unix.restore.setup.VerifyTools as tmpl


def getClass():
	return VerifyTools()


class VerifyTools(tmpl.VerifyTools):

	def run(self, sysdef):
		for device in sysdef.readInfo.getElems("hardware/device"):
			for part in device.getElems("disk-label/partition"):
				fsType = part.get("fs/type")
				if not len(fsType) or not part.get("fs/is-normal"):
					continue
				if fsType not in Constants.FS_MAP:
					raise cairn.Exception("Unknown filesystem type %s for %s found in archive" % (fsType, part.get("device")))
				if not sysdef.info.get(Constants.FS_MAP[fsType]):
					raise cairn.Exception("Failed to find mkfs for filesystem type %s" % (fsType))
		return True
