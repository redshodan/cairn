"""templates.unix.restore.setup.PartDrives Module"""


import cairn



def getClass():
	return PartDrives()


class PartDrives(object):

	def partitionDrive(self, sysdef, drive):
		return


	def run(self, sysdef):
		cairn.log("Partitioning drives")
		for drive in sysdef.readInfo.getElems("hardware/drive"):
			self.partitionDrive(sysdef, drive)
		return True
