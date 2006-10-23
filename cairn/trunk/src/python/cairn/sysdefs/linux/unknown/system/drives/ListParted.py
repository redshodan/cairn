"""linux.unknown.system.drives.ListParted Module"""


import os
import re
import commands

import pylibparted as parted

import cairn
from cairn.sysdefs.linux import Shared



def getClass():
	return ListParted()


class ListParted(object):

	def run(self, sysdef):
		cairn.log("Checking drives")
		try:
			list = parted.probeAllDevices()
			cairn.debug("All drives found: %s" % " ".join(list))
			if not list or not len(list):
				raise cairn.Exception("Failed to find any drives.")
			for device in list:
				pdev = parted.PedDevice(device)
				devShort = device.lstrip("/dev/")
				if not Shared.matchDevice(devShort):
					continue
				cairn.displayRaw("  %s" % devShort)
				drive = sysdef.info.createDriveElem(devShort)
				drive.setChild("device", device)
				drive.setChild("size", "%d" % pdev.getLength())
				drive.setChild("sector-size", "%d" % pdev.getSectorSize())
				model = pdev.getModel()
				if model:
					drive.setChild("model", model)
				chs = pdev.getBiosCHS()
				sysdef.info.createDriveGeomElem(drive, "bios-geom",
												"%d" % chs[0], "%d" % chs[1],
												"%d" % chs[2])
				chs = pdev.getHwCHS()
				sysdef.info.createDriveGeomElem(drive, "hw-geom",
												"%d" % chs[0], "%d" % chs[1],
												"%d" % chs[2])
				empty = False
				try:
					pdev.diskProbe()
				except:
					drive.setChild("empty", "True")
					empty = True
				if not empty:
					pdisk = pdev.diskNew()
					ptype = pdisk.getType()
					drive.setChild("type", ptype.getName())
			cairn.displayNL()
		except Exception, err:
			cairn.displayNL()
			raise cairn.Exception("Failed to probe drives:", err)
		return True
