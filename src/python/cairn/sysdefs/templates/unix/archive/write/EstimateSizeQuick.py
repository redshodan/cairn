"""templates.unix.archive.write.EstimateSizeQuick Module"""


import cairn
from cairn import Options
from cairn.sysdefs.templates.unix.archive.write import EstimateSize as tmpl



def getClass():
	return EstimateSizeQuick()



class EstimateSizeQuick(tmpl.EstimateSize):

	def findTotalSize(self, sysdef, excludes):
		totalSize = long(0)
		for device in sysdef.info.getElems("hardware/device"):
			for partition in device.getElems("disk-label/partition"):
				fs = partition.getElem("fs")
				if fs:
					used = fs.get("used")
					if used:
						totalSize = totalSize + long(used)
		return totalSize * 1048576
