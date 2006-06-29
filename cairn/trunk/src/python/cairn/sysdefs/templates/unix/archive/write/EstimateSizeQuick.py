"""templates.unix.archive.write.EstimateSizeQuick Module"""


import cairn
from cairn import Options
from cairn.sysdefs.templates.unix.archive.write import EstimateSize as tmpl



def getClass():
	return EstimateSizeQuick()



class EstimateSizeQuick(tmpl.EstimateSize):

	def findTotalSize(self, sysdef, excludes):
		totalSize = long(0)
		for drive in sysdef.info.getElems("hardware/drive"):
			for partition in drive.getElems("partition"):
				space = partition.getElem("fs-space")
				if space:
					used = space.get("used")
					totalSize = totalSize + long(used)
		return totalSize * 1048576
